CREATE TABLE "CharacterSet" (
	"Ch_no"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"GameID"	INTEGER NOT NULL,
	"Ch_name"	TEXT NOT NULL,
	"Ch_occupation"	TEXT NOT NULL,
	"Ch_HP"	INTEGER NOT NULL
);