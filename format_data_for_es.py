import json

input_path = 'data/sinhala_songs_corpus.json'
output_path = 'data/sinhala_songs.bulk'

fo = open(input_path, 'r', encoding='utf-8')
json_string = fo.read()
songs_list = json.loads(json_string, strict=False)
fo.close()

fo = open(output_path, 'w', encoding='utf-8')
for song in songs_list:
    while '\n' in song['lyrics']:
        song['lyrics'] = song['lyrics'].replace('\n', '%')
    fo.write('{"index":{ "_index":"songs"}}\n')
    fo.write('{'
             '"track_id":"' + song['track_id'] + '",'
             '"track_name_en":"' + song['track_name_en'] + '",'
             '"track_name_si":"' + song['track_name_si'] + '",'
             '"track_rating":"' + song['track_rating'] + '",'
             '"album_name_en":"' + song['album_name_en'] + '",'
             '"album_name_si":"' + song['album_name_si'] + '",'
             '"artist_name_en":"' + song['artist_name_en'] + '",'
             '"artist_name_si":"' + song['artist_name_si'] + '",'
             '"artist_rating":"' + song['artist_rating'] + '",'
             '"lyrics":"' + song['lyrics'] + '"'
             '}\n')
fo.close()
