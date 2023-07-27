import psycopg2

def insert_table(amount,description, ts):
    --conectar ao banco de dados
    conn = psycopg2.connect(
        host="postgres",
        database="records",
        user="postgres",
        password="123"
    )

    query = "INSERT INTO records (amount,description, ts) VALUES (%s, %s, %s)"

    -- Criar um cursor para executar a consulta
    cur = conn.cursor()
    
    -- Executar a consulta com os valores das variáveis como uma tupla
    cur.execute(query, (id, amount, description, ts))
    
    -- Efetivar as mudanças no banco e fechar a conexão
    conn.commit()
    cur.close()
    conn.close()
