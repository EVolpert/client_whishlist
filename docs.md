# Documentação dos Endpoints

## Login

### Realizar Login

#### Request

```POST /login```

#### Descrição

Permite um usuário existente logar na aplicação.

#### Payload

```
{
    "email": string,
    "name": string
}
```

#### Responses

##### 200

Um JWT que será usado na autenticação de diversos endpoints

```
"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.H5TLs04COMk8hy-nIuBBwS4B_NSfcf5E0MpP86enB8w"
```

##### 401

Quando um login falha por usuário não existir ou dado está faltando

## Customers

### Listar clientes

#### Request
````GET /customers````

#### Descrição

Lista todos os clientes da aplicação

#### Response

##### 200
```
[
    {
        "name": "Teste whishlist",
        "email": "whishlist@teste.com"
    },
    {
        "name": "Test whishlist",
        "email": "teste@teste.com"
    }
]  
```

### Criar clientes

#### Descrição

Cria um cliente que é usado nas views de login e wishlist

#### Request

````POST /customers/````

#### Responses

##### 201

````
{
    "name":"Teste",
    "email":"tes@te.com"
}
````

##### 400

Quando um email já está cadastrado

```
{"email":["customer with this Email already exists."]}
```

Quando um campo está faltando

```
{"name":["This field is required."]}
```

### Detalhe de um cliente

#### Descrição

Trás dados de um cliente específico

#### Request
````GET /customers/<id>/````

#### Headers

```Authorization: <token_gerado_em_login>```

#### Responses

##### 200

```
{
    "name":"Teste",
    "email":"tes@te.com"
}
```

##### 401
Quando o token não bate com o id usado na url

### Atualiza dados de um cliente

#### Descrição

Atualiza dados de um cliente, total ou parcialmente

#### Request
````PUT /customers/<id>/````

#### Headers

```Authorization: <token_gerado_em_login>```

#### Payload
```
{
    "name": "Testando Testinson"
}
```

#### Responses

##### 200

```
{
    "name": ""Testando Testinson"",
    "email": "tes@te.com"
}
```

##### 400
```
{
    "email": [
        "customer with this Email already exists."
    ]
}
```

##### 401

Quando o token não bate com o id usado na url

### Remove dados de um cliente

#### Descrição

Remove dados de um cliente

#### Request
````DELETE /customers/<id>/````

#### Headers

```Authorization: <token_gerado_em_login>```

#### Responses

##### 204

Quando o cliente é removido

##### 401

Quando o token não bate com o id usado na url

## Lista de Desesjos

### Pegar lista de desejos

#### Descrição

Pega a lista de desejo de um usuário específico

#### Request
```
GET /customers/<customer_id>/wishlist
```

#### Headers

```Authorization: <token_gerado_em_login>```

#### Responses

##### 200

```
{
    "id": 3,
    "wishlist": {
        "count": 1,
        "products": [
            {
                "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
                "brand": "bébé confort",
                "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
                "price": 1699.0,
                "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown"
            }
        ]
    },
    "customer": 3
}~~~~
```

##### 401

Quando o token não bate com o id usado na url

##### 404

Quando o cliente não possui uma lista de desejo
```
{
    "detail": "Not found."
} 
```

### Cria ou Atualiza lista de desejos

#### Descrição

Cria ou atualiza uma lista de desejo

#### Request
```
POST /customers/<customer_id>/wishlist/<product_id>
```

#### Headers

```Authorization: <token_gerado_em_login>```

#### Responses

##### 200
````
{
    "id": 3,
    "wishlist": {
        "count": 1,
        "products": [
            {
                "price": 1699.0,
                "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
                "brand": "bébé confort",
                "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
                "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown"
            }
        ]
    },
    "customer": 3
}
````

##### 401

Quando o token não bate com o id usado na url

##### 404

Quando um produto não é encontrado

```
{
    "detail": "Not found."
} 
```

### Remove produto da lista de desejos

#### Descrição

Remove um produto de uma lista de desejo

#### Request
```
DELETE /customers/<customer_id>/wishlist/<product_id>
```

#### Headers

```Authorization: <token_gerado_em_login>```

#### Responses

##### 200
````
{
    "id": 3,
    "wishlist": {
        "count": 0,
        "products": []
    },
    "customer": 3
}
````

##### 401

Quando o token não bate com o id usado na url

##### 404

Quando um produto não é encontrado na lista de desejo

```
{
    "detail": "Not found."
} 
```

### Remove uma lista de desejos

#### Descrição

Remove uma lista de desejo

#### Request
```
DELETE /customers/<customer_id>/wishlist
```

#### Headers

```Authorization: <token_gerado_em_login>```

#### Responses

##### 204
Quando uma lista é deletada com sucesso

##### 401

Quando o token não bate com o id usado na url

##### 404

Quando não é encontrado uma lista de desejo

```
{
    "detail": "Not found."
} 
```