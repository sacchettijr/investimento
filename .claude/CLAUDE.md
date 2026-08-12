<!-- ./.claude/CLAUDE.md -->
# Projeto

API REST para gerenciamento de investimentos desenvolvida em Django.

Este projeto segue arquitetura em camadas, separando responsabilidades entre Models, Services, Serializers e ViewSets.

Toda alteração realizada deve preservar os requisitos descritos no README do projeto.


## Tecnologias

- Python 3.14.6
- Django 6.1
- Django REST Framework
- PostgresSQL
- Docker
- Pytest
- Factory Boy

## Contexto do projeto

Antes de realizar alterações, consulte os arquivos relevantes:

- `.claude/context/architecture.md` → arquitetura e responsabilidades
- `.claude/context/domain.md` → regras do domínio
- `.claude/context/calculations.md` → cálculos financeiros
- `.claude/context/api.md` → endpoints e contratos da API
- `.claude/context/conventions.md` → padrões de código
- `.claude/context/project_state.md` → estado atual do projeto
- `.claude/context/roadmap.md` → funcionalidades planejadas

Não é necessário ler todos os arquivos para toda tarefa.
Leia obrigatoriamente os arquivos relacionados à alteração solicitada.

---

# Arquitetura

A arquitetura deve seguir obrigatóriamente o fluxo:

ViewSet → Serializer → Service → Model

## Responsabilidades

### Models

- Representam apenas dados.
- Não devem conter regras de negócio complexas.
- Apenas validações simples relacionadas à integridade da entidade.

### Services

Toda regra de negócio obrigatóriamente deve ficar em 'services.py'

Exemplo:

- cálculo de rendimento
- cálculo de impostos
- cálculo de saldo
- regras de resgate
- atualização de saldo do usuário

### Serializers

Responsáveis apenas por:

- validação de entrada
- serialização
- desserialização

Nunca implementar regra financeira dentro dos serializers.

### ViewSets

Responsáveis apenas por:

- autenticação
- autorização
- paginação
- filtros
- chamadas aos services

Nunca implementar regra de negócio nas views.

---

# Regras financeiras

Nunca Alterar estas regras sem solicitação explícitas.

## Taxa

Rendimento mensal:

0.52%

Sempre utilizar juros compostos.

Jamais utilizar juros simples.

---

## Datas

Investimento:

- pode ser criado hoje
- pode ser criado no passado
- nunca pode ser criado no futuro

Resgate:

- pode ocorrer hoje
- pode ocorrer no passado
- nunca pode ocorrer no futuro
- nunca pode ocorrer antes da criação do investimento

---

## Valor investido

Nunca permitir:

- valor negativo
- saldo negativo

Sempre utilizar Decimal.

Nunca utilizar float.

---

## Resgate

O resgate sempre corresponde a:

valor investido + rendimento

Não existem resgates parciais.

---

## Tributação

O imposto incida somente sobre os rendimentos.

Jamais aplicar imposto sobre o principal.

Alíquotas:

- menos de 1 ano    → 22.5%
- entre 1 e 2 anos  → 18.5%
- acima de 2 anos   → 15%

---

# Requisitos obrigatórios do projeto

Toda alteração deve manter estes requisitos atendidos.

## Criação de investimento

✔ proprietário
✔ data
✔ valor investido

Validações:

- data <= hoje
- valor >= 0

---

## Consulta

A consulta deve retornar:

- valor investido
- rendimento
- saldo bruto
- imposto
- saldo líquido

Caso exista resgate:

os valores devem ser calculados utilizando a data do resgate.

---

## Resgate

Deve:

- impedir resgates futuros
- impedir resgates antes da criação
- calcular imposto corretamente
- calcular saldo líquido corretamente

---

## Listagem

A listagem deve:

- ser paginada
- listar apenas investimentos do proprietário autenticado
- utilizar OwnerQuerysetMixin quando aplicável

---

# Código

Sempre utilizar:

- type hints
- métodos pequenos
- nomes claros
- baixo acoplamento
- alta coesão
- DRY
- KISS

Evitar comentários desnecessários.

Comentários devem explicar decisões e nunca repetir o código.

---

# Banco de dados

Sempre utilizar:

- transaction.atomic quando necessário
- select_related
- prefetch_related
- QuerySets otimizados

Evitar consultas N+1.

---

# Valores monetários

Obrigatório

```python
Decimal
```

Nunca utilizar:

```python
float
```

Sempre realizar arredondamentos explicitamente utilizando:

```python
quantize()
```

---

# Testes

Toda alteração deve possuir testes.

Prioridade:

1. Services
2. Models
3. Serializers
4. ViewSets

Cobrir:

- casos felizes
- erros
- edge cases
- regras financeiras
- regras tributárias

Nunca remover testes existentes.

---

# Docker

Todos os comandos devem ser executados dentro do container.

Exemplos:

```bash
docker compose exec web python manage.py test

docker compose exec web pytest

docker compose exec web python manage.py makemigrations

docker compose exec web python manage.py migrate
```

---

# Documentação

Toda alteração em endpoints deve manter a documentação atualizada.

Sempre verificar:

- serializers
- exemplos
- parâmetros
- respostas
- códigos HTTP

---

# Checklist obrigatório antes de concluir qualquer tarefa

Antes de considerar uma implementação finalizada, verificar:

- [ ] Projeto executa sem erros.
- [ ] Todos os testes passam.
- [ ] Nenhum requisito do README foi quebrado.
- [ ] Não existe regra financeira nos Serializers.
- [ ] Toda regra financeira está em services.py
- [ ] Todo valor monetário utiliza Decimal
- [ ] Não existe uso de float.
- [ ] Consultas estão otimizadas.
- [ ] Código segue type hints.
- [ ] Endpoint documentado.
- [ ] Testes adicionados ou atualizados.
- [ ] Compatível com Docker.

---

# Preferências deste projeto

Sempre preferir:

- legibilidade ao invés de código extremamente compacto
- simplicidade ao invés de abstrações desnecessárias
- composição ao invés de herança quando possível
- funções pequenas
- responsabilidades únicas
- código explícito

Evitar:

- duplicação
- lógica espalhada
- efeitos colaterais ocultos
- consultas desnecessárias
- otimizações prematuras

---

# Ao responder solicitações

Sempre:

1. Ler os requisitos do README antes de alterar código.
2. Manter compatibilidade com regras financeiras.
3. Não alterar comportamento existente sem justificativa.
4. Preservar compatibilidade com os testes.
5. Caso encontre conflito entre uma solicitação e o README, informar o conflito antes de implementar.
