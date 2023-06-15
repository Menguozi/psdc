-module(sketch_mapper).
-export([initial_state/0,process/3,finished/2]).
-include("debug.hrl").

initial_state() ->
    [ util:uhash_seed(opts:shingle_size()) 
	      || _ <- lists:seq(1,opts:sketch_size()) ].

process({Id,Content}, Seeds, EmitFn) ->
    Shingles = util:shingles(Content),
    Sketches = shingles_to_sketches(Seeds, Shingles), 
    lists:foreach(fun(Sketch) -> EmitFn({Sketch,Id}) end, Sketches),
    Seeds;

process(X,_,_) ->
    io:format("unexpected process ~p\n",[X]).

finished(_,_) ->
     done.

shingles_to_sketches(Seeds, Shingles) ->
    shingles_to_sketches(Seeds, Shingles, []).

shingles_to_sketches([], _Shingles, Sketches) ->
    Sketches;

shingles_to_sketches([Seed|Seeds], Shingles, Sketches) ->
    Sketch = shingles_to_sketch(Seed, Shingles),
    shingles_to_sketches(Seeds, Shingles, [Sketch|Sketches]).

shingles_to_sketch(Seed, Shingles) ->
    Hashes = [ util:uhash(S,Seed) || S <- Shingles ],
    lists:min(Hashes).

    
