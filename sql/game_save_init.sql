CREATE TABLE "GameSave" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"day"	INTEGER NOT NULL,
	"food_supl"	INTEGER NOT NULL,
	"herb_supl"	INTEGER NOT NULL,
	"huts"	INTEGER NOT NULL,
	"temp"	INTEGER NOT NULL,
	"rain"	INTEGER NOT NULL,
	"rain_txt"	TEXT NOT NULL,
	"wind"	INTEGER NOT NULL,
	"wind_txt"	TEXT NOT NULL,
	"user_id"	TEXT UNIQUE,
	"user_pass"	TEXT
);