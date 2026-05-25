-- Seed data: Planes of Power raid targets
-- Table: raid_scheduler_raidtarget
-- Columns: name, description, zone, target_type, is_active
--
-- target_type values:
--   boss    — single named boss kill
--   event   — structured event / trial / quest encounter
--   farming — kill generic/unnamed mobs for drops or quest completion
--
-- Covers every flagging step tracked by the PoP Flags Checker
-- (Seer Mal Nae'Shi / zone_flags progression).
--
-- Run against the default app database.

-- ============================================================
-- Tier 1 — Plane of Justice
-- Any one of the six trials completes the PoJ flag chain.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('PoJ Trial of Execution',  'One of six PoJ trials. Complete any trial, loot a Mark, present to the Tribunal, then return to Mavuin to finish the Tier 1 PoJ flag chain.', 'Plane of Justice', 'event', 1),
  ('PoJ Trial of Hanging',    'One of six PoJ trials. Complete any trial, loot a Mark, present to the Tribunal, then return to Mavuin to finish the Tier 1 PoJ flag chain.', 'Plane of Justice', 'event', 1),
  ('PoJ Trial of Larceny',    'One of six PoJ trials. Complete any trial, loot a Mark, present to the Tribunal, then return to Mavuin to finish the Tier 1 PoJ flag chain.', 'Plane of Justice', 'event', 1),
  ('PoJ Trial of Perversion', 'One of six PoJ trials. Complete any trial, loot a Mark, present to the Tribunal, then return to Mavuin to finish the Tier 1 PoJ flag chain.', 'Plane of Justice', 'event', 1),
  ('PoJ Trial of Torture',    'One of six PoJ trials. Complete any trial, loot a Mark, present to the Tribunal, then return to Mavuin to finish the Tier 1 PoJ flag chain.', 'Plane of Justice', 'event', 1),
  ('PoJ Trial of Three',      'One of six PoJ trials. Complete any trial, loot a Mark, present to the Tribunal, then return to Mavuin to finish the Tier 1 PoJ flag chain.', 'Plane of Justice', 'event', 1);

-- ============================================================
-- Tier 1 — Plane of Disease
-- Grummus kill opens Crypt of Decay. Bertoxxulous is in CoD, not PoD.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Grummus', 'Plane of Disease — Grummus the Polluted. Killing him opens the Crypt of Decay and starts the Bertoxxulous flag chain. Turn in the ward to Adler Fuirstel afterward.', 'Plane of Disease', 'boss', 1);

-- ============================================================
-- Tier 1 — Plane of Nightmare
-- The Hedge Event must be completed before Terris Thule becomes accessible.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Hedge Event',   'Plane of Nightmare — Kill the Construct of Nightmares in the hedge maze to complete the Thelin pre-flag. Required before Terris Thule''s lair (PoN B) becomes accessible.', 'Plane of Nightmare', 'event', 1),
  ('Terris Thule',  'Plane of Nightmare — Mistress of Nightmares. Final boss of PoN B. Kill requires Hedge Event completion. Hail Poxbourne in PoTranquility afterward to complete the flag.', 'Plane of Nightmare', 'boss',  1);

-- ============================================================
-- Tier 1 — Plane of Innovation
-- Manaetic Behemoth unlocks Plane of Tactics access (Giwin flagging).
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Manaetic Behemoth', 'Plane of Innovation — Final boss construct. Killing the Behemoth triggers the Giwin flag chain, granting access to Plane of Tactics (Drunder).', 'Plane of Innovation', 'boss', 1);

-- ============================================================
-- Tier 2 — Plane of Valor
-- Aerin'Dar kill required to access Halls of Honor.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Aerin''Dar', 'Plane of Valor — Prismatic dragon. Killing Aerin''Dar and completing the follow-up with the Tribunal grants access to Halls of Honor.', 'Plane of Valor', 'boss', 1);

-- ============================================================
-- Tier 2 — Plane of Storms
-- Two-part Askr quest. Part 1 is an NPC encounter; Part 2 requires
-- killing storm giants throughout the zone to complete the quest
-- and receive the Talisman of Thunderous Foyer (Bastion of Thunder key).
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('PoS Askr Quest — Giant Hunt', 'Plane of Storms — Complete Part 1 with Askr, then kill storm giants throughout the zone to finish Part 2 and receive the Talisman of Thunderous Foyer (Bastion of Thunder access). Generic giants, not a single named target.', 'Plane of Storms', 'farming', 1);

-- ============================================================
-- Tier 2 — Crypt of Decay
-- Bertoxxulous is in Crypt of Decay, NOT Plane of Disease.
-- Flag chain: kill Bertox → hail planar projection → talk to Adler Fuirstel.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Bertoxxulous', 'Crypt of Decay — The Plaguebringer. Required for Plane of Torment access. After the kill, hail the planar projection, then talk to Adler Fuirstel in PoTranquility to complete the flag chain.', 'Crypt of Decay', 'boss', 1);

-- ============================================================
-- Tier 2 — Plane of Torment
-- Keeper of Sorrows is a required mid-boss before Saryrn.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Keeper of Sorrows', 'Plane of Torment — Required mid-boss before Saryrn becomes accessible. Part of the Tylis / Shadyglade flag chain.', 'Plane of Torment', 'boss', 1),
  ('Saryrn',            'Plane of Torment — Mistress of Pain. Final boss of Plane of Torment. Kill and hail the planar projection, then talk to Shadyglade in PoTranquility to complete the Tier 2 flag.', 'Plane of Torment', 'boss', 1);

-- ============================================================
-- Tier 3 — Plane of Tactics (Drunder)
-- All three Zek bosses required. After each kill, get the language
-- translation done by Librarian Maelin (combined flag steps).
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Tallon Zek',             'Plane of Tactics — Twin war god. Required Tier 3 kill. Loot the pouches for the Maelin translation step (combined flag chain).', 'Plane of Tactics', 'boss', 1),
  ('Vallon Zek',             'Plane of Tactics — Twin war god. Required Tier 3 kill. Loot the pouches for the Maelin translation step (combined flag chain).', 'Plane of Tactics', 'boss', 1),
  ('Rallos Zek the Warlord', 'Plane of Tactics — Final boss of Drunder. Required for Tier 3 combined flags. Parchments reference the Manaetic Behemoth.', 'Plane of Tactics', 'boss', 1);

-- ============================================================
-- Tier 3 — Bastion of Thunder
-- Agnarr the Storm Lord. Pre-steps involve talking to Karana in-zone.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Agnarr the Storm Lord', 'Bastion of Thunder — Final boss. Requires Askr Talisman to enter. Talk to Karana in-zone before the pull. Killing Agnarr is required for the Tier 3 combined flag chain.', 'Bastion of Thunder', 'boss', 1);

-- ============================================================
-- Tier 3 — Halls of Honor
-- Three separate trials, each given by a different NPC.
-- All three required before Temple of Marr becomes accessible.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('HoH Trial 1: Rydda''Dar',  'Halls of Honor — First trial, given by Faye. Defeat Rydda''Dar. All three HoH trials must be completed before Temple of Marr access is granted.', 'Halls of Honor', 'event', 1),
  ('HoH Trial 2: Villagers',   'Halls of Honor — Second trial, given by Rhaliq Trell. Save the villagers. All three HoH trials must be completed before Temple of Marr access is granted.', 'Halls of Honor', 'event', 1),
  ('HoH Trial 3: Nomads',      'Halls of Honor — Third trial, given by Alekson Garn. Defeat the nomads. All three HoH trials must be completed before Temple of Marr access is granted.', 'Halls of Honor', 'event', 1);

-- ============================================================
-- Tier 3b — Temple of Marr
-- Mithaniel Marr kill completes the Tier 3b flag.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Mithaniel Marr', 'Temple of Marr — Lord of Valor. Required for the Tier 3 combined flag chain. Killing Marr and completing the follow-up unlocks the Cipher of the Divine Language step.', 'Temple of Marr', 'boss', 1);

-- ============================================================
-- Tier 3 — Tower of Solusek Ro
-- Six mini-bosses must all be killed before Solusek Ro spawns.
-- Entry to the Tower requires Combined flag 2 + full Tier 1-3 completion.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Arlyxir',               'Tower of Solusek Ro — One of six mini-bosses that must be cleared before Solusek Ro spawns. Grants the "wealth of knowledge" flag memory.', 'Tower of Solusek Ro', 'boss', 1),
  ('Jiva',                  'Tower of Solusek Ro — One of six mini-bosses that must be cleared before Solusek Ro spawns. Grants the "strength" flag memory.', 'Tower of Solusek Ro', 'boss', 1),
  ('Protector of Dresolik', 'Tower of Solusek Ro — One of six mini-bosses that must be cleared before Solusek Ro spawns. Grants the "power surges" flag memory.', 'Tower of Solusek Ro', 'boss', 1),
  ('Xuzl',                  'Tower of Solusek Ro — One of six mini-bosses that must be cleared before Solusek Ro spawns. Grants the "arcane wisdom" flag memory.', 'Tower of Solusek Ro', 'boss', 1),
  ('Rizlona',               'Tower of Solusek Ro — One of six mini-bosses that must be cleared before Solusek Ro spawns. Grants the "song" flag memory.', 'Tower of Solusek Ro', 'boss', 1),
  ('Solusek Ro',            'Tower of Solusek Ro — The Burning Prince. Final boss of the Tower. Killing Solusek Ro and completing the Maelin elemental flag step opens Plane of Fire access.', 'Tower of Solusek Ro', 'boss', 1);

-- ============================================================
-- Tier 4 — Elemental Planes
-- All four elemental bosses required for Plane of Time access.
-- Entry to the elementals requires the Librarian Maelin combined flag.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Fennin Ro',                  'Plane of Fire (Doomfire) — Tyrant of Fire. One of four elemental bosses required for Plane of Time access.', 'Plane of Fire',  'boss',  1),
  ('Xegony the Queen of Air',    'Plane of Air (Eryslai) — One of four elemental bosses required for Plane of Time access.', 'Plane of Air',   'boss',  1),
  ('The Rathe Council',          'Plane of Earth (Vegarlson) — 12-member council event. All members must be killed near-simultaneously. One of four elemental bosses required for Plane of Time access.', 'Plane of Earth', 'event', 1),
  ('Coirnav the Avatar of Water','Plane of Water (Reef of Coirnav) — One of four elemental bosses required for Plane of Time access.', 'Plane of Water', 'boss',  1);

-- ============================================================
-- Tier 5 — Plane of Time
-- Phase A re-fights all Tier 2/3/4 bosses. Phase B culminates in Quarm.
-- ============================================================
INSERT INTO raid_scheduler_raidtarget (name, description, zone, target_type, is_active) VALUES
  ('Plane of Time Phase A', 'Plane of Time — Phase A event. Sequential re-fights against Saryrn, Terris Thule, Tallon Zek, Vallon Zek, Rallos Zek the Warlord, Fennin Ro, Coirnav, Xegony, and the Rathe Council.', 'Plane of Time', 'event', 1),
  ('Quarm',                 'Plane of Time — Phase B final boss. The end goal of Planes of Power progression. Killing Quarm and completing the PoTime flag allows future characters to skip straight to elemental access.', 'Plane of Time', 'boss',  1);
