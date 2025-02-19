// Algoritmo para validação de cadeias de caracteres com base em um Autômato Finito Não Determinístico

#include "afn.h"

int main() {
    #undef DISPLAY_LOG
    #define DISPLAY_LOG false // controla os detalhes de operação no console

    AFN afn(
        {
            { "q0", 'a', "q1" },
            { "q1", 'a', "q1" },
            { "q1", 'b', "q2" },
            { "q2", 'a', "q2" },
            { "q2", 'b', "q2" },
            { "q2", 'a', "q3" },
        },
        "q0",
        { "q3" }
    );

    afn.print();

    afn.validarCadeia("ababa");
    afn.validarCadeia("abab");
    afn.validarCadeia("baa");
    afn.validarCadeia("aaaaaaaaaaabaaaaaaaaaa");

    return 0;
}