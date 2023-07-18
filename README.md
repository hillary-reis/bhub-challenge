# bhub-api-challenge
Build a simple CRUD API to control BHub customers


## dependencias

### criando venv
com makefile
```bash
cd src/

make create-venv
```

rodando cada comando
```bash
cd src/

pyenv shell 3.11.1
poetry env use 3.11.1

poetry shell
```

### instalação das dependências do projeto
```bash
poetry install
```

### atualização das dependências do projeto, caso necessário
```bash
poetry update
```

## rodando a aplicação

### é possível rodar a aplicação de duas formas:

* fazendo o build da imagem e rodando com o docker-compose
    ```bash
    docker-compose up --build -d
    ```

* Criando um container para o banco de dados e rodando a API local
    ```bash
    docker run --name bhub_challenge \
                    -p 5432:5432 \
                    -e POSTGRES_PASSWORD=bhub \
                    -e POSTGRES_USER=bhub \
                    -e POSTGRES_HOST_AUTH_METHOD=trust \
                    -e POSTGRES_DB=bhub \
                    -d postgres
    ```

    ```bash
    uvicorn app:app --reload
    ```


### criando as tabelas e suas relações
```bash
CREATE TABLE public.customers (
	id serial4 NOT NULL,
	uuid varchar(36) NOT NULL,
	created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	company_name varchar(100) NOT NULL,
	phone_number varchar(15) NOT NULL,
	address varchar(100) NOT NULL,
	billing integer NOT NULL,
	CONSTRAINT customers_pkey PRIMARY KEY (id)
);
```

```bash
CREATE TABLE public.bank_data (
	id serial4 NOT NULL,
	uuid varchar(36) NOT NULL,
	created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	agency varchar(5) NOT NULL,
	account varchar(9) NOT NULL,
	bank varchar(100) NOT NULL,
	customer_id int4 NOT NULL,
	CONSTRAINT bank_data_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_bank_data_customer_id ON public.bank_data USING btree (customer_id);
ALTER TABLE public.bank_data ADD CONSTRAINT bank_data_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);
```

### enquando o projeto estiver rodando, é possível visualizar a documentação na url abaixo
```bash
http://localhost:8080/docs
```

## makefile

### validar lint
```bash
make .flake
```

### validar segurança do código
```bash
make .bandit
```

### rodar todos os testes e receber um relatório da cobertura
```bash
make test
```

### remover todos os arquivos de cache
```bash
make clean
```
