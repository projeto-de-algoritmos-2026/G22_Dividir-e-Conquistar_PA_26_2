# CensuradorStrassen

**Conteúdo da Disciplina**: Dividir e Conquistar<br>

## Alunos

|Matrícula | Aluno |
| -- | -- |
| 21/1062179  |  Marcelo de Araújo Lopes |
| 17/0020339  |  Paulo Lucca |

## Sobre

O projeto borra rostos em fotos usando multiplicação de matrizes. A imagem é
uma matriz de pixels, e borrar uma região é multiplicá-la por uma matriz de
média. Essas multiplicações são feitas com o **algoritmo de Strassen**, que
divide cada matriz em quatro blocos e resolve o produto com 7 multiplicações
recursivas em vez de 8.

## Instalação

**Linguagem**: Python 3.10+<br>
**Framework**: Streamlit<br>

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G22_Dividir-e-Conquistar_PA_26_2.git
cd G22_Dividir-e-Conquistar_PA_26_2
pip install -r requirements.txt
```
