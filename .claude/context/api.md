// ./.claude/context/api.md

Todos os endpoints abaixo estão sob o prefixo `/api/` e exigem autenticação
(Session ou Basic), exceto quando indicado.

## Investimentos

### POST /api/investimentos/

Cria um investimento para o usuário autenticado.

Body:
- `descricao` (opcional)
- `valor_investido` (obrigatório, Decimal > 0)
- `data_inicio` (obrigatório, <= hoje)

O `usuario` é sempre o usuário autenticado (não é aceito no body).

### GET /api/investimentos/

Lista os investimentos do usuário autenticado (paginado, `IsOwnerOrSuperUser`
via queryset). Superusuários veem todos.

### GET /api/investimentos/{id}/

Consulta um investimento. Retorna:
- `valor_investido`
- `rendimento`
- `saldo_bruto`
- `imposto`
- `saldo_liquido`
- `montante`, `aliquota`, `resgatado`, `data_final`

Se o investimento já foi resgatado, os valores são calculados na
`data_resgate`; caso contrário, na data atual.

## Resgates

### POST /api/resgates/

Resgata um investimento do usuário autenticado.

Body:
- `investimento` (obrigatório, id de um investimento do próprio usuário)
- `data_resgate` (opcional, default = hoje; não pode ser futura nem anterior
  à criação do investimento)

Regras (validadas no Model, traduzidas para 400 pelo
`core.api.exceptions.exception_handler`):
- impede resgates futuros;
- impede resgates antes da criação do investimento;
- impede um segundo resgate para o mesmo investimento;
- calcula imposto e saldo líquido via `InvestimentoService`.

### GET /api/resgates/

Lista os resgates dos investimentos do usuário autenticado.

### GET /api/resgates/{id}/

Consulta um resgate específico.

## Usuários

### POST /api/usuario/

Cria um usuário (`AllowAny`). Dispara e-mail de confirmação de cadastro.

### GET /api/usuario/

Lista usuários (apenas o próprio usuário, exceto superusuário).

### GET /api/usuario/{id}/

### GET /api/usuario/me/

Dados do usuário autenticado.

### GET /api/usuario/saldo/

Saldo do usuário autenticado (soma dos investimentos não resgatados).
Requer e-mail verificado (`IsVerifiedEmail`).
