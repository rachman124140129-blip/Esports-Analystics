-- 1. Mendaftarkan Hero ONIC (Jika belum ada)
INSERT INTO game_entities (entity_id, name, game, entity_type) 
VALUES 
    (901, 'Fanny', 'Mobile Legends', 'Hero'),     
    (902, 'Valentina', 'Mobile Legends', 'Hero'), 
    (903, 'Khufra', 'Mobile Legends', 'Hero'),    
    (904, 'Claude', 'Mobile Legends', 'Hero'),    
    (905, 'Paquito', 'Mobile Legends', 'Hero')    
ON CONFLICT DO NOTHING;

-- 2. Memasukkan Performa ONIC (Dynamic Mapping)
INSERT INTO player_performance (match_id, player_id, team_id, entity_id, kills, deaths, assists, kda_ratio) 
SELECT 7002, 401, 400, entity_id, 11, 1, 7, 18.00 FROM game_entities WHERE name = 'Fanny' AND game = 'Mobile Legends'
UNION ALL
SELECT 7002, 402, 400, entity_id, 6, 0, 11, 17.00 FROM game_entities WHERE name = 'Valentina' AND game = 'Mobile Legends'
UNION ALL
SELECT 7002, 403, 400, entity_id, 1, 3, 16, 5.67 FROM game_entities WHERE name = 'Khufra' AND game = 'Mobile Legends'
UNION ALL
SELECT 7002, 404, 400, entity_id, 8, 2, 5, 6.50 FROM game_entities WHERE name = 'Claude' AND game = 'Mobile Legends'
UNION ALL
SELECT 7002, 405, 400, entity_id, 5, 2, 6, 5.50 FROM game_entities WHERE name = 'Paquito' AND game = 'Mobile Legends';