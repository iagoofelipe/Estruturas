#include "afn.h"
#include <iostream>
#include <algorithm> // std::find

#define DISPLAY_LOG false

template <typename T>
bool vectorHasValue(std::vector<T>* vector, T value) {
    auto it = std::find(vector->begin(), vector->end(), value);
    return it != vector->end();
}

Estado::Estado(std::string nomeEstado, bool final)
    : nome(nomeEstado)
    , final(final)
{}

std::string Estado::getNome() { return nome; }
bool Estado::isFinal() { return final; }

void Estado::print() {
    std::cout << "Estado e conexoes:\n\t<Estado nome=" << getNome() << " final=" << isFinal() << ">\n";
    for(const auto& par : conexoes)
        for(const auto& e : conexoes[par.first])
            std::cout << "\t<Conexao simbolo=" << par.first << " estado=" << e->getNome() << ">\n";

}

void Estado::addConexao(char simbolo, Estado* proximo) {
    if(DISPLAY_LOG)
        std::cout << "gerando producao: " << getNome() << " -> " << simbolo << proximo->getNome() << std::endl;

    if(!conexoes.count(simbolo))
        conexoes[simbolo] = std::vector<Estado*>();

    conexoes[simbolo].push_back(proximo);
}

bool Estado::verificarSimbolo(char simbolo, std::vector<Estado*>* fila) {
    bool valido = conexoes.count(simbolo);
    if(DISPLAY_LOG)
        std::cout << "simbolo '" << simbolo << "' " << (valido? "valido" : "invalido") << " para o estado " << nome << std::endl;

    if(!valido)
        return false;


    for(auto const& e : conexoes[simbolo]) {
        fila->push_back(e);
    }

    return true;
}

AFN::AFN(std::vector<relacaoEstado> regras, std::string inicial, std::vector<std::string> finais) {
    std::cout << std::boolalpha;

    for(const auto& r : regras) {
        // gerando estado inicial
        if(!estados.count(r.inicial))
            estados[r.inicial] = new Estado(r.inicial, vectorHasValue<std::string>(&finais, r.inicial));

        // gerando estado final
        if(!estados.count(r.final))
            estados[r.final] = new Estado(r.final, vectorHasValue<std::string>(&finais, r.final));

        // conectando estados
        estados[r.inicial]->addConexao(r.simbolo, estados[r.final]);
    }

    if(!estados.count(inicial)) {
        std::cout << "o estado inicial '" << inicial << "' nao esta na relacao de regras!\n";
        exit(-1);
    }

    this->inicial = estados[inicial];
}

AFN::~AFN() {
    for(const auto& par : estados)
        delete par.second;
}

bool AFN::validarCadeia(std::string cadeia) {
    std::vector<Estado*> aux1 { inicial }, aux2;
    bool auxFila = false, valid;
    std::vector<Estado*>* fila = &aux1;

    if(DISPLAY_LOG)
        std::cout << "validando a cadeia '" << cadeia << "'...\n";

    for(const auto& c : cadeia) {

        // verificando valor para todos os estados da fila
        valid = false;
        auxFila = !auxFila;
        std::vector<Estado*>* proximaFila = auxFila? &aux2 : &aux1;
        proximaFila->clear();

        for(const auto& e : *fila) {
            if(e->verificarSimbolo(c, proximaFila))
                valid = true;
        }

        fila = auxFila? &aux2 : &aux1;

        if(!valid)
            break;
    }

    // caso tenha verificado toda a cadeia sem erro, verificando se é um estado final válido
    if(valid) {
        valid = false;
        for(const auto& e : *fila) {
            if(e->isFinal()) {
                valid = true;
                break;
            }
        }

        if(DISPLAY_LOG)
            std::cout << "cadeia verificada " << (valid? "com" : "sem") << " um estado final na fila de estados\n";
    }

    std::cout << "A cadeia '" << cadeia << "' e " << (valid? "valida" : "invalida") << " para o AFN\n";
    return valid;
}

void AFN::print() {
    for(const auto& par : estados)
        par.second->print();
}