# Estruturas
Repositório para estruturas e conceitos construídos com POO.

# Tópicos
- [ANFs](#afns)

# AFNs
Autômatos Finitos Não Determinísticos são modelos computacionais utilizados em processos como validação de expressões/gramáticas regulares, 
os quais permitem a análise de uma cadeia a partir de um conjunto de estados finitos e um alfabeto.

O algoritmo foi escrito em C++ e permite a validação de cadeias de caracteres a partir de uma estrutura de Autômato Finito válida. O exemplo foi baseado no modelo:
![AFN](imgs/afn.png)
> Exemplo de Autômato Finito Não Determinístico

Analogamente, no modelo em C++ [`afn\main.cpp`](afn/main.cpp) foi representado utilizado uma `struct` e `std::vector`:
```C++
// definindo estrutura do AFN
std::vector<relacaoEstado> regras {
    { "q0", 'a', "q1" },
    { "q1", 'a', "q1" },
    { "q1", 'b', "q2" },
    { "q2", 'a', "q2" },
    { "q2", 'b', "q2" },
    { "q2", 'a', "q3" },
};
std::string inicial = "q0";
std::vector<std::string> finais { "q3" };
```
