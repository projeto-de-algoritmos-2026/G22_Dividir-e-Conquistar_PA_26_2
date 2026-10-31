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

Arquivos:

1. **Strassen** (`strassen.py`): multiplicação de matrizes com Strassen e, para
   comparação, a versão dividir e conquistar clássica, com 8 subproblemas.
2. **Borrão** (`borrao.py`): monta a matriz de média e borra uma região da imagem.
3. **Interface** (`app.py`): app em Streamlit para enviar a foto, marcar o rosto,
   borrar e comparar os dois algoritmos.

### Algoritmo: Strassen

Para multiplicar `A · B`, as duas matrizes são divididas em quatro blocos de
metade do tamanho:

```
A = | A11 A12 |    B = | B11 B12 |
    | A21 A22 |        | B21 B22 |
```

A forma direta precisa de 8 produtos de blocos (`A11·B11 + A12·B21`, e assim por
diante). Strassen calcula 7 produtos auxiliares:

```
M1 = (A11 + A22)(B11 + B22)     M5 = (A11 + A12) B22
M2 = (A21 + A22) B11            M6 = (A21 − A11)(B11 + B12)
M3 = A11 (B12 − B22)            M7 = (A12 − A22)(B21 + B22)
M4 = A22 (B21 − B11)
```

e monta o resultado só com somas:

```
C11 = M1 + M4 − M5 + M7      C12 = M3 + M5
C21 = M2 + M4                C22 = M1 − M2 + M3 + M6
```

**Complexidade.** A recorrência é `T(n) = 7 T(n/2) + O(n²)`, que dá
`O(n^log2(7)) ≈ O(n^2,81)`. A versão clássica, `T(n) = 8 T(n/2) + O(n²)`, fica em
`O(n³)`.

**Detalhes da implementação.**

- As matrizes são completadas com zeros até o lado virar uma potência de 2, para
  que a divisão em 4 blocos sempre seja exata.
- Quando o lado chega no **caso base** (parâmetro `corte`), o produto é feito
  direto com o numpy. Em Python, a recursão até matrizes 1×1 seria lenta demais.

### Borrão como multiplicação de matrizes

O borrão usado é a média dos vizinhos (box blur). Para uma região `R` com `h`
linhas e `w` colunas:

1. `B_h` é uma matriz `h × h` em que a linha `i` tem o valor `1/k` nas colunas
   vizinhas de `i` (até `raio` de distância) e zero no resto. `k` é o número de
   vizinhos.
2. `B_h · R` troca cada pixel pela média dos vizinhos **na vertical**.
3. Multiplicar por `B_wᵀ` à direita faz o mesmo **na horizontal**.

O resultado é `B_h · R · B_wᵀ`, calculado com dois produtos de Strassen para cada
canal de cor (vermelho, verde e azul).

## Instalação

**Linguagem**: Python 3.10+<br>
**Framework**: Streamlit<br>

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G22_Dividir-e-Conquistar_PA_26_2.git
cd G22_Dividir-e-Conquistar_PA_26_2
pip install -r requirements.txt
```

## Uso

Abrir a interface:

```bash
streamlit run app.py
```

No navegador:

1. Envie uma foto.
2. Ajuste os sliders da barra lateral até o retângulo vermelho cobrir o rosto.
3. Escolha a intensidade do borrão.
4. Use **Comparar** para medir o Strassen contra o dividir e conquistar clássico.

Rodar os testes:

```bash
python -m pytest
```

## Screenshots

<!-- TODO: adicionar prints da interface em docs/screenshots/ -->

## Vídeo

<!-- TODO: link da apresentação -->

## Outros

- Fotos com mais de 600 pixels de largura são reduzidas para o borrão rodar rápido.
- Os testes comparam o Strassen com a multiplicação do numpy (`A @ B`).
