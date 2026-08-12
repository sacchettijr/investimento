# Projeto de Teste Back-End <img src="https://coderockr.com/assets/images/coderockr.svg" align="right" height="50px" />

Encare este desafio como uma oportunidade para criar uma aplicação seguindo as melhores práticas modernas de desenvolvimento (utilizando a stack de sua preferência). Ao mesmo tempo, sinta-se à vontade para utilizar sua própria arquitetura, padrões de código, organização do projeto e bibliotecas de terceiros. É perfeitamente aceitável utilizar código puro (vanilla) ou qualquer framework e bibliotecas.

## Escopo

Neste desafio, você deverá desenvolver uma API para uma aplicação de gerenciamento de investimentos, contendo as seguintes funcionalidades:

1. **Criação** de um investimento contendo proprietário, data de criação e valor investido.
    1. A data de criação do investimento pode ser a data atual ou qualquer data passada.
    2. Um investimento não pode ser nem se tornar negativo.

2. **Consulta** de um investimento, exibindo o valor inicial e o saldo esperado.
    1. O saldo esperado deve ser a soma do valor investido com os [rendimentos][].
    2. Caso o investimento já tenha sido resgatado, o saldo deverá refletir os rendimentos obtidos até a data do resgate.

3. **Resgate** de um investimento.
    1. O resgate será sempre correspondente ao valor inicial investido acrescido dos rendimentos. Resgates parciais não são suportados.
    2. O resgate pode ocorrer em qualquer data passada ou na data atual, desde que não seja anterior à criação do investimento nem em uma data futura.
    3. Os [impostos][taxes] devem ser aplicados ao resgate antes da apresentação do valor final.

4. **Listagem** dos investimentos de uma pessoa.
    1. A listagem deve possuir paginação.

> **Observação:** A implementação de uma interface gráfica **não será avaliada**.

## Cálculo dos Rendimentos

O investimento renderá **0,52% ao mês**, sempre no mesmo dia em que foi criado.

Como o rendimento é pago mensalmente, ele deve ser tratado como **juros compostos**, ou seja, a cada novo período (mês), o rendimento obtido passa a fazer parte do saldo do investimento e também renderá nos meses seguintes.

## Tributação

Ao realizar o resgate de um investimento, incidem impostos. A tributação deve ser aplicada **apenas sobre o lucro (rendimentos)** obtido.

Por exemplo:

- Valor investido: **R$ 1.000,00**
- Saldo atual: **R$ 1.200,00**

Nesse caso, os impostos serão aplicados apenas sobre os **R$ 200,00** de lucro.

A alíquota varia de acordo com o tempo de existência do investimento:

- Se possuir **menos de um ano**, a alíquota será de **22,5%** (imposto = **R$ 45,00**).
- Se possuir **entre um e dois anos**, a alíquota será de **18,5%** (imposto = **R$ 37,00**).
- Se possuir **mais de dois anos**, a alíquota será de **15%** (imposto = **R$ 30,00**).

## Requisitos

1. Desenvolver o projeto utilizando qualquer tecnologia de sua preferência. É perfeitamente aceitável utilizar código puro ou qualquer framework e bibliotecas.
2. Embora seja permitido utilizar quantas dependências desejar, elas devem ser escolhidas com critério.
3. Não é obrigatório implementar o envio de e-mails de notificação, porém o código necessário para isso será considerado um diferencial.
4. A API deve estar documentada de alguma forma.

## Entrega

O código-fonte do projeto e suas dependências deverão estar disponíveis no GitHub.

Siga os passos abaixo:

1. Faça um **fork** deste repositório para sua conta no GitHub (caso ainda não possua uma conta, será necessário criar uma).
2. Crie uma branch chamada **development** e realize todos os commits nela. **Não envie código para a branch main.**
3. Inclua um arquivo **README** contendo:
    - Instruções especiais para compilação ou execução, caso existam;
    - Lista das bibliotecas de terceiros utilizadas e uma breve descrição do motivo de sua utilização;
    - Um link para a documentação da API.
4. Quando concluir o projeto, abra um **Pull Request** da branch **development** para **main** e envie o link.
5. Evite realizar commits muito grandes que escondam sua evolução durante o desenvolvimento. Fique à vontade para trabalhar em uma branch separada e utilizar `git rebase` para organizar seus commits antes da entrega final.

## Padrões de Código

Durante o desenvolvimento, procure manter o código o mais limpo, organizado e consistente possível.

## Prazo do Projeto

O ideal é concluir este desafio em até **5 dias**. Não deve ser necessário mais do que **uma semana** para finalizá-lo.

## Garantia de Qualidade

Utilize a lista abaixo para verificar a qualidade do projeto.

### Geral

- Antes de tudo, a aplicação deve executar sem erros.
- Todos os requisitos descritos acima foram atendidos?
- O padrão de código está consistente?
- A API está bem documentada?
- A API possui testes unitários?

## Envio

1. Envie o link do repositório no GitHub.
2. Descreva brevemente como escolheu as ferramentas utilizadas no projeto.

## Divirta-se Programando 🤘

- A descrição deste desafio é propositalmente vaga em alguns aspectos. Caso tenha dúvidas, sinta-se à vontade para pedir esclarecimentos.
- Se algum dos requisitos estiver acima do seu nível atual de conhecimento, você pode deixá-lo de lado, mas lembre-se de mencionar isso no Pull Request.

## Créditos

Este desafio de programação foi inspirado em:

https://github.com/kinvoapp/kinvo-back-end-test

[rendimentos]: #cálculo-dos-rendimentos
[taxes]: #tributação
[interest]: #cálculo-de-juros
[juros compostos]: https://www.investopedia.com/terms/g/gain.asp