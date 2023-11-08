# Workshop Quantum Espresso no cluster Carbono (**Em desenvolvimento**)

Tutorial pratico de como utilizar o Quantum Espresso para rodar cálculos de estrutura eletrônica padrões como otimização estrutural, densidade de carga, estrutura de bandas eletrônicas e densidade de estados (total e parcial).

## Tutorial 1: Estrutura eletrônica do grafeno

Para calcular a estrutura eletrônica de um cristal, é preciso se certificar de que a estrutura está bem otimizada, ou seja, precisamos garantir que a estrutura esteja com a simetria e os parâmetros de rede corretos. Isso pode ser garantido conduzindo cálculos de otimização de geometria como o **relax** e o **vc-relax**. 

- Relax: cálculo de otimização de geometria baseado na minimização da energia total, forças e estresse na estrutura. Esta otimização ocorre da seguinte forma: um cálculo auto-consistente é feito para obter a densidade de carga e consequentemente a energia da estrutura (Teorema de Hohenberg-Kohn). Com a energia, as forças entre os átomos é calculada por meio do teorema de Hellmann-Feynman. Caso os critérios de convergência (energia e forças) não sejam satisfeitos, os átomos são movidos (seguindo um esquema de minimização como o gradiente conjugado, por exemplo). Um novo cálculo auto-consistente é feito com os átomos nas novas posições e o procedimento é repetido até que todos os critérios de convergência sejam satisfeitos.

- Vc-relax: o procedimento feito pelo espresso para minimizar a energia e força da estrutura é semelhante ao relax, mas com o adicional de que agora, os parâmetros de rede são modificados para auxiliar no processo de minimização.

Com a geometria da estrutura devidamente otimizada, podemos iniciar o procedimento de cálculo de estrutura eletrônica.

(mostrar como visualizar a estrutura do material utilizando o xcrysden ou outro software parecido).

```
calculation = 'scf'
```

### Procedimento

#### SCF

Nesta etapa, será calculada a densidade eletrônica do sistema. 

(adicionar o input do espresso)

#### NSCF

Nesta etapa, será feito um cálculo sob potencial constante (calculado na etapa anterior). Nesta etapa, a flag **calculation** deve ser setada para *’nscf’* outro ponto importante é que nesta etapa deve ser especificado o número de bandas deve ser especidicado de acordo com o tipo de sistema por meio da flag **nbnd**. É importante que nesta etapa, o grid de pontos-k utilizado seja mais denso que na etapa de anterior. Outro ponto importante, é que para cálculos de densidade de estados (DOS), as ocupações devem ser setadas para o método *’tetrahedra’*, por meio da flag **occupations**. Em caso de sistemas com baixa simetria, é aconselhável utilizar a flag **nosym** = *’true’*.

**Importante**: o prefixo utilizado (flag **prefix**) e a flag **outdir** devem ser as mesmas que na etapa anterior. Também, as posições atômicas utilizadas são as da etapa anterior.

(adicionar o input do espresso destacando as flags importantes)

### BANDAS

As bandas eletrônicas são calculadas de fato na etapa do NSCF para todos os pontos-kgerados. Entretante, é muito comum estudar a relação de dispersão E(k) ao longo de caminhos que passam por pontos de alta simetria na zona de Brillouin do cristal. Esse cálculo pode ser feito definindo a tag **calculation** como *’bands’*.

**importante**: Nesta etapa, os pontos-k devem ser definidos como **crystal_b** e como coordenadas desses pontos de alta simetria na zona de Brilloiun.

(adicionar o input do espresso)

### Densidade de Estados (DOS):

Nesta etapa, utilizamos o código **dos.x** ou **projwfc.x**. No primeiro caso, é calculada apenas a densidade de estados total é calculada, enquanto o segundo código é utilizado para projetar essa densidade em diferentes orbitais dos elementos químicos da estrututras.

(adicionar o input do espresso)
