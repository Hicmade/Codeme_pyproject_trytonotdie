CREATE TABLE "Users" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"User_id"	TEXT NOT NULL,
	"User_pass"	TEXT NOT NULL,
	"Game_id"	INTEGER NOT NULL
);