CREATE TABLE IF NOT EXISTS hits (
  id INTEGER PRIMARY KEY, ts TEXT, method TEXT, path TEXT, query TEXT, via TEXT,
  ua TEXT, agent TEXT, kind TEXT, accept TEXT, referer TEXT, country TEXT,
  asn INTEGER, as_org TEXT, ip_hash TEXT, signed TEXT
);
CREATE INDEX IF NOT EXISTS hits_ts ON hits(ts);
CREATE TABLE IF NOT EXISTS guestbook (
  id INTEGER PRIMARY KEY, ts TEXT, agent_name TEXT, model TEXT, operator TEXT,
  how_found TEXT, note TEXT, via TEXT, ua TEXT, agent TEXT, ip_hash TEXT
);
CREATE TABLE IF NOT EXISTS answers (
  id INTEGER PRIMARY KEY, ts TEXT, task TEXT, answer TEXT, correct INTEGER,
  agent_name TEXT, via TEXT, ua TEXT, agent TEXT, ip_hash TEXT
);
