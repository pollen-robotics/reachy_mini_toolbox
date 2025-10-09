# Moves utils scripts

## Record moves library

Run `record_move.py` to start recording a move. This will listen to current ongoing movements on your robot and record them. 

```bash
python3 record_move.py -l <library_name> -n <move_name>
```
- `-l` `library_name` : the name of the library you want your move to be recorded to (e.g. `dances`).
- `-n` `move_name` : the name of the move you are going to record (e.g. `samba`).

For example :

```bash
python3 record_move.py -l <dances> -n <samba>
python3 record_move.py -l <dances> -n <salsa>
python3 record_move.py -l <dances> -n <rumba>
...
```

For now, everything is recorded locally in the `library_name` directory. When you are ready, you can upload your dataset to the hub. 

## Make and upload the moves library

You first need to be authentified on the Hub. Run `hf auth login` if you haven't already.

Then you can run:

```bash
python3 make_move_library.py --repo_id <username>/<library_name> -l <library_name>/ 
```

For example : 

```bash
python3 make_move_library.py --repo_id pollen-robotics/dances -l dances/ 
```

- `-l` is the path to the local library

You can always come back and record new moves in your library and re-upload them using the same command. This will update your dataset on the hub.
