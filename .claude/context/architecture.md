# Arquitetura do Projeto

## 1. Objetivo

Este documento descreve a arquitetura, organização, responsabilidades e regras de dependência do projeto.

O projeto é uma API REST para gerenciamento de investimentos, desenvolvida com Django e Django REST Framework, executada em ambiente Docker e utilizando PostgreSQL.

Este arquivo deve ser utilizado como referência antes de qualquer alteração estrutural ou implementação de nova funcionalidade.

A arquitetura existente deve ser respeitada.

Não realizar reorganizações, renomeações ou mudanças arquiteturais apenas por preferência pessoal.

---

# 2. Stack

Principais tecnologias:

* Python 3.14.6
* Django 6.1
* Django REST Framework
* PostgreSQL
* Docker
* Pytest
* Factory Boy

Ferramentas e configurações adicionais podem ser encontradas em:

```text
pyproject.toml
requirements.txt
requirements_dev.txt
docker-compose.yml
Dockerfile
```

---

# 3. Estrutura do repositório

A estrutura atual do repositório é:

```text
.
├── .claude/
│   ├── commands/
│   │   ├── refactor.md
│   │   ├── release.md
│   │   ├── review.md
│   │   └── tests.md
│   │
│   ├── context/
│   │   ├── api.md
│   │   ├── architecture.md
│   │   ├── calculations.md
│   │   ├── conventions.md
│   │   ├── domain.md
│   │   ├── project_state.md
│   │   └── roadmap.md
│   │
│   ├── CLAUDE.md
│   └── settings.json
│
├── .vscode/
│   └── settings.json
│
├── django/
│   ├── core/
│   ├── investimento/
│   ├── usuario/
│   ├── PROJETO/
│   ├── utils/
│   ├── static/
│   ├── templates/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── manage.py
│   ├── requirements.txt
│   └── requirements_dev.txt
│
├── .dockerignore
├── .env
├── .gitignore
├── dev_build.cmd
├── dev_reset.cmd
├── dev_start.cmd
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── README_pt-br.md
```

---

# 4. Organização geral

O código Django está localizado dentro da pasta:

```text
django/
```

A aplicação está dividida em três apps principais:

```text
core
usuario
investimento
```

O pacote:

```text
PROJETO
```

contém a configuração global do Django.

A organização segue uma separação entre:

```text
Infraestrutura
    ↓
Configuração Django
    ↓
Aplicações de domínio
    ↓
API
    ↓
Regras de negócio
    ↓
Persistência
```

---

# 5. Aplicação `core`

A aplicação `core` contém funcionalidades compartilhadas e infraestrutura comum utilizada por outras partes do projeto.

Estrutura:

```text
core/
├── admin/
│   ├── __init__.py
│   ├── base.py
│   └── mixins.py
│
├── api/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── filters.py
│   ├── mixins.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── responses.py
│   ├── serializers.py
│   ├── urls.py
│   └── viewsets.py
│
├── management/
│   └── commands/
│       ├── __init__.py
│       └── create_admin.py
│
├── migrations/
│   └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_models.py
│
├── __init__.py
├── admin.py
├── apps.py
├── current_user.py
├── forms.py
├── middleware.py
├── models.py
├── urls.py
└── views.py
```

## Responsabilidades do `core`

O `core` deve concentrar funcionalidades que sejam realmente compartilhadas entre diferentes domínios.

Exemplos:

* classes base;
* mixins;
* middleware;
* usuário corrente;
* filtros;
* paginação;
* permissões genéricas;
* respostas HTTP;
* exceções;
* serializers base;
* ViewSets base;
* comandos administrativos compartilhados.

---

# 6. `core/admin`

```text
core/admin/
├── __init__.py
├── base.py
└── mixins.py
```

Contém abstrações relacionadas ao Django Admin.

Responsabilidades:

* classes base para Admin;
* mixins administrativos;
* comportamentos administrativos reutilizáveis.

Não colocar regras de negócio financeiro neste diretório.

Quando uma operação administrativa precisar executar uma regra de negócio, reutilizar o service correspondente.

---

# 7. `core/api`

```text
core/api/
├── exceptions.py
├── filters.py
├── mixins.py
├── pagination.py
├── permissions.py
├── responses.py
├── serializers.py
├── urls.py
└── viewsets.py
```

Este diretório representa a camada de infraestrutura compartilhada da API.

## `exceptions.py`

Exceções reutilizáveis da API.

Não criar exceções duplicadas dentro das aplicações quando uma exceção genérica existente puder ser reutilizada.

## `filters.py`

Filtros reutilizáveis.

Filtros específicos de um domínio devem permanecer próximos ao domínio quando não fizerem sentido para outras aplicações.

## `mixins.py`

Mixins compartilhados pela API.

Antes de criar um novo mixin em `usuario/api` ou `investimento/api`, verificar se o comportamento deve ser genérico e pertencer ao `core`.

## `pagination.py`

Configurações e classes de paginação compartilhadas.

A listagem de investimentos deve utilizar a infraestrutura de paginação existente.

## `permissions.py`

Permissões genéricas da API.

Permissões específicas de usuário podem permanecer em `usuario/api/permissions.py`.

## `responses.py`

Padronização de respostas HTTP da API.

Evitar criar formatos de resposta incompatíveis com os padrões existentes.

## `serializers.py`

Serializers base e comportamentos compartilhados.

Não duplicar lógica existente nos serializers específicos.

## `viewsets.py`

ViewSets base e comportamentos compartilhados.

ViewSets de domínio devem reutilizar essas abstrações quando aplicável.

---

# 8. Aplicação `investimento`

A aplicação `investimento` representa o principal domínio de negócio do projeto.

Estrutura:

```text
investimento/
├── api/
│   ├── __init__.py
│   ├── serializers.py
│   ├── urls.py
│   └── viewsets.py
│
├── migrations/
│   └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_models.py
│
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── services.py
├── tests.py
└── views.py
```

## Responsabilidades

A aplicação é responsável por:

* investimentos;
* rendimentos;
* juros compostos;
* resgates;
* tributação;
* saldo bruto;
* saldo líquido;
* demonstrativo financeiro;
* regras relacionadas ao ciclo de vida do investimento.

---

# 9. `investimento/models.py`

Os models representam as entidades persistidas relacionadas ao domínio financeiro.

Os models devem permanecer enxutos.

Eles podem conter:

* campos;
* relacionamentos;
* propriedades simples;
* métodos diretamente relacionados ao estado da entidade;
* validações de integridade;
* comportamentos simples de persistência.

Não colocar cálculos financeiros complexos diretamente nos models.

Não duplicar regras existentes no service.

---

# 10. `investimento/services.py`

Este é o principal ponto da arquitetura para regras de negócio financeiro.

Toda regra financeira complexa deve ser implementada e centralizada em `services.py`.

Responsabilidades incluem:

* cálculo do rendimento;
* juros compostos;
* cálculo do montante;
* cálculo do saldo;
* cálculo de demonstrativo;
* cálculo de imposto;
* determinação de alíquota;
* cálculo de saldo bruto;
* cálculo de saldo líquido;
* regras de resgate;
* regras relacionadas ao período do investimento.

## Regra fundamental

Nunca duplicar cálculos financeiros em:

```text
serializers.py
viewsets.py
views.py
models.py
admin.py
tests.py
```

Quando uma regra já estiver implementada no service, reutilizá-la.

---

# 11. Camada de serviço

O fluxo esperado para operações de negócio é:

```text
ViewSet
   ↓
Serializer
   ↓
Service
   ↓
Model
   ↓
Database
```

O Service é responsável por coordenar regras que envolvam uma ou mais entidades.

O Service deve ser independente da camada HTTP sempre que possível.

Não utilizar objetos de request diretamente em regras de domínio.

Evitar acoplamento desnecessário entre services e DRF.

---

# 12. `investimento/api`

```text
investimento/api/
├── __init__.py
├── serializers.py
├── urls.py
└── viewsets.py
```

Representa a camada REST específica de investimentos.

---

# 13. `investimento/api/serializers.py`

Responsabilidades:

* validar dados de entrada;
* converter dados;
* serializar entidades;
* apresentar informações da API;
* executar validações relacionadas à entrada.

O serializer pode validar regras simples de entrada.

Exemplos:

* campo obrigatório;
* formato;
* tipo;
* valor permitido;
* presença de relacionamento.

Entretanto, regras financeiras complexas devem ser delegadas ao service.

Não calcular rendimento manualmente no serializer.

Não calcular imposto manualmente no serializer.

Não duplicar regras de resgate no serializer.

---

# 14. `investimento/api/viewsets.py`

O ViewSet representa a camada HTTP da aplicação.

Responsabilidades:

* receber requisições;
* autenticação;
* autorização;
* seleção do queryset;
* seleção do serializer;
* chamar services;
* retornar respostas;
* utilizar paginação;
* utilizar filtros.

Não colocar no ViewSet:

* cálculo de rendimento;
* cálculo de imposto;
* cálculo de juros;
* regras financeiras;
* regras complexas de resgate.

O ViewSet deve orquestrar a operação.

---

# 15. `investimento/api/urls.py`

Responsável exclusivamente pelo roteamento da API de investimentos.

As URLs específicas de investimento devem permanecer aqui.

Não colocar lógica de negócio nas URLs.

---

# 16. Aplicação `usuario`

A aplicação `usuario` representa o domínio dos usuários.

Estrutura:

```text
usuario/
├── api/
│   ├── __init__.py
│   ├── mixins.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── viewsets.py
│
├── migrations/
│   └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_models.py
│
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
├── utils.py
└── views.py
```

Responsabilidades:

* usuário;
* autenticação;
* autorização específica;
* saldo do usuário;
* API de usuários;
* funcionalidades relacionadas à conta do usuário.

---

# 17. `usuario/models.py`

Contém as entidades persistidas relacionadas aos usuários.

O modelo de usuário pode manter comportamentos simples diretamente relacionados ao seu estado.

Regras complexas que envolvam múltiplos domínios devem ser avaliadas para implementação em services.

Não duplicar regras financeiras.

---

# 18. `usuario/api`

Contém a camada REST específica do usuário.

```text
usuario/api/
├── mixins.py
├── permissions.py
├── serializers.py
├── urls.py
└── viewsets.py
```

Componentes específicos do domínio de usuário permanecem aqui.

Componentes genéricos devem permanecer em `core/api`.

---

# 19. Isolamento por proprietário

Recursos pertencentes a usuários devem respeitar o proprietário autenticado.

O usuário nunca deve conseguir:

* consultar investimento de outro usuário;
* alterar investimento de outro usuário;
* resgatar investimento de outro usuário;
* acessar informações privadas de outro usuário.

Utilizar as abstrações existentes para isolamento por proprietário, especialmente:

```text
OwnerQuerysetMixin
```

quando aplicável.

A filtragem por proprietário deve ocorrer no queryset e/ou camada apropriada de autorização.

Não confiar apenas no frontend para garantir isolamento.

---

# 20. Aplicação `PROJETO`

```text
PROJETO/
├── api/
│   ├── __init__.py
│   └── urls.py
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
└── wsgi.py
```

Contém a configuração global do Django.

---

# 21. `PROJETO/settings.py`

Responsável por:

* configurações Django;
* aplicações;
* middleware;
* banco de dados;
* REST Framework;
* templates;
* arquivos estáticos;
* configurações de segurança;
* variáveis de ambiente;
* configurações de infraestrutura.

Não colocar regras de negócio em `settings.py`.

---

# 22. `PROJETO/urls.py`

Responsável pelo roteamento global.

As URLs específicas devem permanecer nas aplicações.

A estrutura deve seguir aproximadamente:

```text
PROJETO/urls.py
      ↓
application urls.py
      ↓
api urls.py
```

Não colocar regras de negócio no roteamento.

---

# 23. `PROJETO/api`

```text
PROJETO/api/
├── __init__.py
└── urls.py
```

Responsável pelo agrupamento ou roteamento global da API.

Não colocar implementação de endpoints neste diretório.

---

# 24. `utils`

```text
utils/
├── __init__.py
└── env.py
```

Contém utilidades relacionadas à infraestrutura/configuração.

Utilitários devem permanecer genéricos.

Não utilizar `utils` como local genérico para qualquer código que não tenha outra localização.

Evitar criar um arquivo `utils.py` apenas para evitar decidir onde determinada lógica pertence.

---

# 25. Templates e arquivos estáticos

```text
templates/
└── registration/
    ├── base.html
    └── login.html

static/
```

Esses diretórios pertencem à camada de apresentação HTML tradicional do Django.

A API REST não deve depender de templates para retornar seus dados.

---

# 26. `forms.py` e `views.py`

As aplicações possuem:

```text
forms.py
views.py
```

Esses componentes representam funcionalidades tradicionais do Django.

Para endpoints REST, utilizar:

```text
api/serializers.py
api/viewsets.py
api/urls.py
```

Não criar uma implementação REST paralela utilizando views tradicionais quando a funcionalidade puder ser implementada na arquitetura DRF existente.

---

# 27. Django Admin

Cada aplicação pode possuir seu próprio:

```text
admin.py
```

O Admin é uma interface administrativa.

Não deve conter uma segunda implementação das regras de negócio.

Se uma operação administrativa precisar executar uma regra existente, reutilizar o service.

---

# 28. Management Commands

Comandos administrativos ficam em:

```text
core/management/commands/
```

Atualmente:

```text
create_admin.py
```

Management commands podem orquestrar operações administrativas, mas não devem duplicar regras de negócio existentes.

---

# 29. Testes

Os testes estão organizados por aplicação:

```text
core/tests/
investimento/tests/
usuario/tests/
```

Testes atuais incluem:

```text
test_api.py
test_models.py
```

As alterações devem preservar e ampliar a cobertura existente.

---

# 30. Estratégia de testes

A prioridade dos testes deve ser:

```text
Regras de negócio
       ↓
Services
       ↓
Models
       ↓
Serializers
       ↓
API / ViewSets
```

Testes devem cobrir:

* comportamento esperado;
* validações;
* erros;
* casos extremos;
* regras financeiras;
* tributação;
* datas;
* isolamento por proprietário;
* resgate;
* paginação.

Não remover um teste apenas porque ele dificulta uma implementação.

Quando o comportamento esperado mudar, atualizar o teste de acordo com a nova regra explicitamente aprovada.

---

# 31. Migrations

Cada aplicação mantém suas próprias migrations:

```text
core/migrations/
investimento/migrations/
usuario/migrations/
```

Alterações em models devem gerar novas migrations.

Não editar migrations antigas já aplicadas sem necessidade explícita.

Antes de alterar schema:

1. verificar migrations existentes;
2. verificar testes;
3. verificar relacionamentos;
4. avaliar impacto nos dados.

---

# 32. Banco de dados

O projeto utiliza PostgreSQL.

A camada de persistência deve ser acessada através do ORM do Django.

Preferir:

```python
QuerySet
```

a SQL manual quando o ORM for suficiente.

SQL explícito somente quando houver justificativa técnica.

---

# 33. Performance

Sempre avaliar:

```python
select_related()
prefetch_related()
```

quando houver relacionamentos.

Evitar:

* N+1 queries;
* consultas repetitivas;
* carregar dados desnecessários;
* executar lógica de filtragem em Python quando puder ser executada no banco.

Filtros devem preferencialmente ser realizados pelo banco.

---

# 34. Transações

Operações que alterem múltiplas entidades relacionadas devem utilizar:

```python
transaction.atomic()
```

quando necessário para garantir consistência.

Especialmente operações como:

```text
Resgate
    ↓
Atualização do investimento
    ↓
Registro do resgate
    ↓
Atualização do saldo do usuário
```

devem ser analisadas quanto à necessidade de atomicidade.

Não utilizar transações indiscriminadamente.

---

# 35. Valores monetários

Todo valor financeiro deve utilizar:

```python
Decimal
```

Nunca utilizar:

```python
float
```

para valores monetários.

Arredondamentos financeiros devem ser explícitos.

Preferir:

```python
Decimal.quantize()
```

com estratégia de arredondamento definida.

---

# 36. Dependências

Dependências de produção ficam em:

```text
requirements.txt
```

Dependências de desenvolvimento ficam em:

```text
requirements_dev.txt
```

Antes de adicionar uma biblioteca:

1. verificar se a funcionalidade já existe;
2. verificar se o Django/DRF já oferece solução;
3. avaliar complexidade adicionada;
4. avaliar manutenção;
5. avaliar compatibilidade;
6. adicionar somente se houver benefício real.

Evitar dependências desnecessárias.

---

# 37. Docker

Arquivos relacionados:

```text
Dockerfile
docker-compose.yml
entrypoint.sh
```

O ambiente de desenvolvimento deve utilizar Docker conforme a configuração atual do projeto.

Comandos Django devem preferencialmente ser executados dentro do container.

Exemplo:

```bash
docker compose exec <service> python manage.py test
```

O nome do serviço deve ser confirmado no `docker-compose.yml`.

Não assumir que o nome do container é `django`.

---

# 38. Variáveis de ambiente

Variáveis específicas do ambiente devem ser configuradas através de:

```text
.env
```

e acessadas por:

```text
utils/env.py
```

ou pela configuração apropriada do Django.

Nunca inserir credenciais diretamente no código.

Nunca expor:

* SECRET_KEY;
* senhas;
* tokens;
* credenciais;
* chaves privadas.

---

# 39. Scripts de desenvolvimento

Existem scripts:

```text
dev_build.cmd
dev_reset.cmd
dev_start.cmd
```

Antes de criar um novo script para uma tarefa existente, verificar se esses scripts já fornecem a funcionalidade necessária.

---

# 40. Documentação

A documentação principal está em:

```text
README.md
README_pt-br.md
```

A documentação deve refletir o estado real da aplicação.

Alterações significativas devem avaliar a necessidade de atualizar:

* endpoints;
* exemplos;
* instalação;
* execução;
* dependências;
* regras de negócio;
* documentação da API.

---

# 41. Regras de dependência entre camadas

A direção preferencial das dependências é:

```text
API
 ↓
Service
 ↓
Model
 ↓
Database
```

Configurações:

```text
PROJETO
 ↓
Applications
```

Componentes compartilhados:

```text
core
 ↑
usuario
 ↑
investimento
```

Na prática, `core` deve fornecer infraestrutura compartilhada e não depender de regras específicas de `investimento`.

Evitar dependências circulares.

---

# 42. Regra para criação de novos arquivos

Antes de criar um arquivo:

1. verificar se já existe arquivo com responsabilidade semelhante;
2. verificar se a funcionalidade pertence a `core`;
3. verificar se pertence a uma aplicação específica;
4. verificar se deve ser um service;
5. verificar se deve ser um serializer;
6. verificar se deve ser um mixin;
7. verificar se deve ser uma permission;
8. somente então criar o arquivo.

Evitar arquivos genéricos sem responsabilidade clara.

---

# 43. Regra para reutilização

Antes de implementar qualquer funcionalidade:

```text
1. Procurar código existente.
2. Procurar abstração existente.
3. Procurar service existente.
4. Procurar mixin existente.
5. Procurar permission existente.
6. Procurar serializer base.
7. Procurar ViewSet base.
8. Reutilizar quando possível.
9. Criar nova implementação somente quando necessário.
```

A duplicação deve ser evitada.

---

# 44. Regra para alterações

Antes de modificar código:

```text
1. Identificar o domínio.
2. Identificar a camada.
3. Ler os arquivos relacionados.
4. Procurar implementações semelhantes.
5. Ler os testes existentes.
6. Ler o contexto relevante em .claude/context/.
7. Implementar a menor alteração necessária.
8. Executar os testes.
9. Revisar possíveis efeitos colaterais.
10. Atualizar documentação quando necessário.
```

---

# 45. Alterações arquiteturais

Não realizar alterações estruturais sem necessidade.

Evitar mudanças como:

* mover aplicações;
* renomear módulos;
* alterar arquitetura;
* criar novas camadas;
* substituir abstrações;
* criar novos padrões;

quando a implementação atual já atende ao requisito.

Se uma alteração arquitetural for necessária:

1. explicar o problema;
2. explicar a solução;
3. identificar impacto;
4. atualizar testes;
5. atualizar documentação;
6. atualizar os arquivos de contexto.

---

# 46. Regra de compatibilidade

Qualquer alteração deve preservar:

* regras do domínio;
* contratos da API;
* segurança;
* isolamento por proprietário;
* testes existentes;
* compatibilidade com Docker;
* documentação.

Uma melhoria de código não justifica quebrar comportamento existente sem uma mudança de requisito.

---

# 47. Princípios arquiteturais

Priorizar:

1. Correção.
2. Segurança.
3. Integridade dos dados.
4. Clareza.
5. Testabilidade.
6. Baixo acoplamento.
7. Alta coesão.
8. Reutilização.
9. Performance.
10. Simplicidade.

Evitar:

* overengineering;
* abstrações prematuras;
* duplicação;
* lógica espalhada;
* dependências circulares;
* regras de negócio na camada HTTP;
* cálculos financeiros duplicados.

---

# 48. Regra fundamental

O projeto já possui uma arquitetura definida.

O objetivo de novas implementações não é reconstruir a arquitetura.

O objetivo é evoluir a arquitetura existente de maneira incremental, consistente e compatível.

Antes de criar uma nova solução, o código existente deve ser compreendido.

A solução mais simples que respeitar as regras do projeto deve ser preferida.
