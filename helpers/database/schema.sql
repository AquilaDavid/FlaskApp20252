CREATE TABLE IF NOT EXISTS instituicoes_ensino (
    co_entidade      BIGINT NOT NULL,
    no_entidade      TEXT NOT NULL,

    sg_uf            VARCHAR(2) NOT NULL,
    co_uf            INTEGER NOT NULL,

    no_municipio     TEXT,
    co_municipio     BIGINT,

    nu_ano_censo     INTEGER NOT NULL,

    qt_mat_bas       INTEGER DEFAULT 0,
    qt_mat_prof      INTEGER DEFAULT 0,
    qt_mat_eja       INTEGER DEFAULT 0,
    qt_mat_esp       INTEGER DEFAULT 0,

    qt_mat_fund      INTEGER DEFAULT 0,
    qt_mat_inf       INTEGER DEFAULT 0,
    qt_mat_med       INTEGER DEFAULT 0,

    qt_mat_zr_na     INTEGER DEFAULT 0,
    qt_mat_zr_rur    INTEGER DEFAULT 0,
    qt_mat_zr_urb    INTEGER DEFAULT 0,

    qt_mat_total     INTEGER DEFAULT 0,

    CONSTRAINT pk_instituicoes_ensino
        PRIMARY KEY (co_entidade, nu_ano_censo)
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_ie_ano
    ON instituicoes_ensino (nu_ano_censo);

CREATE INDEX IF NOT EXISTS idx_ie_uf
    ON instituicoes_ensino (sg_uf);

CREATE INDEX IF NOT EXISTS idx_ie_municipio
    ON instituicoes_ensino (co_municipio);
