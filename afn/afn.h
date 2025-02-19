#include <string>
#include <vector>
#include <map>

template <typename T>
bool vectorHasValue(std::vector<T>* vector, T value);

class Estado {

public:
    Estado(std::string nomeEstado, bool final=false);

    std::string getNome();
    bool isFinal();
    void print();
    void addConexao(char simbolo, Estado* proximo);
    bool verificarSimbolo(char simbolo, std::vector<Estado*>* fila);

private:
    std::string nome;
    bool final;
    std::map<char, std::vector<Estado*>> conexoes;

};

struct relacaoEstado {
    std::string inicial;
    char simbolo;
    std::string final;
};

class AFN {

public:
    AFN(std::vector<relacaoEstado> regras, std::string inicial, std::vector<std::string> finais);
    ~AFN();
    bool validarCadeia(std::string cadeia);
    void print();

private:
    std::map<std::string, Estado*> estados;
    Estado* inicial;
};