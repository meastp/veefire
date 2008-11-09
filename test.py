from api.dbapi import Show, Episode, Season, Database
from backends.imdbtv import Backend as imdbtvbackend

Showlist = [ Show( "Black Books", "30", "ext3" , "imdbtvbackend", "tt0262150" ) ]#,
#                 Show( "The IT Crowd", "30", "ext3" , "imdbtvbackend", "tt0487831" ) ,
#                 Show( "Life on Mars", "60", "ext3" , "imdbtvbackend", "tt0478942" ) ,
#                 Show( "Chuck", "60", "ext3" , "imdbtvbackend", "tt0934814" ) ,
#                 Show( "M*A*S*H", "60", "ext3" , "imdbtvbackend", "tt0068098" ),
#                 Show( "My Name Is Earl", "30", "ext3" , "imdbtvbackend", "tt0460091" ) ]

backend = imdbtvbackend()

DB = backend.updateShows( Showlist )

DB.printDb()
