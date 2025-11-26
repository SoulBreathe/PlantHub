import sqlite3


def popular_banco(connection: sqlite3.Connection):
    cursor = connection.cursor()

    # Verifica se já existem dados para não duplicar
    # Se quiseres forçar o reset dos dados PADRÃO (não do usuário),
    # podes descomentar as linhas de DELETE abaixo (Cuidado com IDs):

    # cursor.execute("DELETE FROM Especies")
    # cursor.execute("DELETE FROM PragasDoencas")
    # cursor.execute("DELETE FROM DiagnosticoPerguntas")
    # cursor.execute("DELETE FROM DiagnosticoRespostas")
    # cursor.execute("DELETE FROM DiagnosticoMapeamento")

    # -------------------------------------------------------------------------
    # 1. ESPÉCIES (Plantas Comuns)
    # -------------------------------------------------------------------------
    cursor.execute("SELECT COUNT(*) FROM Especies")
    if cursor.fetchone()[0] == 0:
        print("🌱 Populando Espécies...")
        especies = [
            (
                "Tomate",
                "Solanum lycopersicum",
                "Regular (mantenha úmido)",
                "Sol Pleno (6h+)",
                "Remover chupões",
                "Rico em Potássio",
                "Primavera",
                "assets/especies/tomate.png",
            ),
            (
                "Hortelã",
                "Mentha sp.",
                "Diária (gosta de água)",
                "Sombra Parcial",
                "Poda de contenção",
                "Orgânico/Humus",
                "Ano todo",
                "assets/especies/hortela.png",
            ),
            (
                "Suculenta",
                "Echeveria sp.",
                "Pouca (só quando seco)",
                "Sol ou Claridade",
                "Retirar folhas secas",
                "Específico cactos",
                "Verão",
                "assets/especies/suculenta.png",
            ),
            (
                "Manjericão",
                "Ocimum basilicum",
                "Regular",
                "Sol Pleno",
                "Cortar flores",
                "Nitrogênio",
                "Verão",
                "assets/especies/manjericao.png",
            ),
            (
                "Jibóia",
                "Epipremnum aureum",
                "Moderada",
                "Sombra/Luz Indireta",
                "Limpeza de folhas",
                "NPK 10-10-10",
                "Ano todo",
                "assets/especies/jiboia.png",
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO Especies (nome_popular, nome_cientifico, instrucoes_rega, necessidade_sol, necessidade_poda, uso_adubos, epoca_plantio, foto_exemplo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            especies,
        )

    # -------------------------------------------------------------------------
    # 2. PRAGAS & DOENÇAS (Base de Conhecimento)
    # -------------------------------------------------------------------------
    cursor.execute("SELECT COUNT(*) FROM PragasDoencas")
    if cursor.fetchone()[0] == 0:
        print("🐛 Populando Pragas...")
        # Nota: A ordem de inserção define o ID (1, 2, 3...). Usaremos isso no diagnóstico.
        pragas = [
            # ID 1: Pulgão
            (
                "Pulgão",
                "Insetos pequenos (verdes/pretos) que sugam a seiva.",
                "Folhas enroladas, amareladas e pegajosas.",
                "Óleo de Neem ou calda de sabão.",
                "assets/pragas/pulgao.png",
            ),
            # ID 2: Cochonilha
            (
                "Cochonilha",
                "Parece algodão branco ou escamas nos caules.",
                "Manchas brancas, planta fraca, formigas.",
                "Cotonete com álcool ou óleo mineral.",
                "assets/pragas/cochonilha.png",
            ),
            # ID 3: Fungo (Oídio)
            (
                "Oídio (Fungo)",
                "Pó branco sobre as folhas.",
                "Parece talco nas folhas, inibe fotossíntese.",
                "Leite cru diluído (10%) ou fungicida.",
                "assets/pragas/oidio.png",
            ),
            # ID 4: Lagarta
            (
                "Lagarta",
                "Larvas que comem folhas.",
                "Buracos grandes nas folhas e fezes pretas.",
                "Remoção manual ou Bacillus thuringiensis.",
                "assets/pragas/lagarta.png",
            ),
            # ID 5: Falta de Água (Não é praga, mas é diagnóstico)
            (
                "Falta de Água",
                "Desidratação da planta.",
                "Folhas murchas, secas e quebradiças.",
                "Regue imediatamente e verifique o solo.",
                "assets/pragas/seca.png",
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO PragasDoencas (nome_comum, descricao, sintomas, tratamento, foto_exemplo)
            VALUES (?, ?, ?, ?, ?)
        """,
            pragas,
        )

    # -------------------------------------------------------------------------
    # 3. DIAGNÓSTICO (Árvore de Decisão)
    # -------------------------------------------------------------------------
    # Estrutura Lógica:
    # P1: O que você vê?
    #    - Algo branco/algodonoso -> É Cochonilha (ID 2) ou Oídio (ID 3)? -> P2
    #    - Insetos visíveis -> P3
    #    - Folhas com defeito (sem bichos) -> P4

    cursor.execute("SELECT COUNT(*) FROM DiagnosticoPerguntas")
    if cursor.fetchone()[0] == 0:
        print("🩺 Criando Árvore de Diagnóstico...")

        # --- PERGUNTAS ---
        ps = [
            (1, "O que você nota visualmente na planta?"),
            (2, "Esse 'branco' parece algodão ou pó?"),
            (3, "Como são esses insetos?"),
            (4, "Como estão as folhas?"),
        ]
        cursor.executemany(
            "INSERT INTO DiagnosticoPerguntas (ordem, texto_pergunta) VALUES (?, ?)", ps
        )

        # --- RESPOSTAS & FLUXO ---
        # id_proxima_pergunta: NULL se for um diagnóstico final (mapeamento)

        # Respostas da P1 (Visual Geral)
        r_p1 = [
            ("Manchas ou estruturas brancas", 1, 2),  # Vai para P2
            ("Vejo insetos caminhando/voando", 1, 3),  # Vai para P3
            ("Folhas com buracos ou murchas", 1, 4),  # Vai para P4
        ]

        # Respostas da P2 (Branco)
        r_p2 = [
            ("Parece algodão/teia (Cochonilha)", 2, None),  # Fim -> Mapear para Praga 2
            (
                "Parece talco/pó espalhado (Oídio)",
                2,
                None,
            ),  # Fim -> Mapear para Praga 3
        ]

        # Respostas da P3 (Insetos)
        r_p3 = [
            (
                "Pequenos, verdes ou pretos, aos montes",
                3,
                None,
            ),  # Fim -> Mapear para Praga 1 (Pulgão)
            (
                "Grandes/Larvas comendo folhas",
                3,
                None,
            ),  # Fim -> Mapear para Praga 4 (Lagarta)
        ]

        # Respostas da P4 (Folhas)
        r_p4 = [
            (
                "Murchas e terra seca",
                4,
                None,
            ),  # Fim -> Mapear para Praga 5 (Falta água)
            (
                "Com grandes buracos mordidos",
                4,
                None,
            ),  # Fim -> Mapear para Praga 4 (Lagarta)
        ]

        todas_respostas = r_p1 + r_p2 + r_p3 + r_p4

        # Inserir Respostas
        cursor.executemany(
            """
            INSERT INTO DiagnosticoRespostas (texto_resposta, id_pergunta, id_proxima_pergunta)
            VALUES (?, ?, ?)
        """,
            todas_respostas,
        )

        # Precisamos pegar os IDs das respostas inseridas para fazer o mapeamento
        # Como o SQLite autoincrementa, assumimos a ordem de inserção:
        # P1: IDs 1, 2, 3
        # P2: IDs 4, 5
        # P3: IDs 6, 7
        # P4: IDs 8, 9

        # --- MAPEAMENTO (Resposta ID -> Praga ID) ---
        # ID Pragas: 1=Pulgão, 2=Cochonilha, 3=Oídio, 4=Lagarta, 5=Seca
        mapeamentos = [
            (4, 2),  # Algodão -> Cochonilha
            (5, 3),  # Pó -> Oídio
            (6, 1),  # Pequenos verdes -> Pulgão
            (7, 4),  # Grandes -> Lagarta
            (8, 5),  # Murchas -> Seca
            (9, 4),  # Buracos -> Lagarta
        ]

        cursor.executemany(
            "INSERT INTO DiagnosticoMapeamento (id_resposta, id_praga) VALUES (?, ?)",
            mapeamentos,
        )

    connection.commit()
