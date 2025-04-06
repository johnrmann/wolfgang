# Wolfgang

Transformer-based music generation.

# Running Wolfgang

## Installation

TK

## Running the App

After installing everything, run the API with the following command...

```
cd python
uvicorn api.app:app
```

Run the React client with the following command...

```
cd wolfgang
pnpm start
```

## Training the Model

TK

# Technical Info

## Basic Definitions

Throughout this project, you may encounter the following terms...

1. A ***beat*** is a musical unit of time. Many songs will have 120 beats per minute, and will have one beat equal a quarter note.
2. A ***tick*** is Wolfgang's fundamental unit of time. We divide a beat into `12 ticks`.
	1. The rationale for this is that we don't expect to go beyond a sixteenth note, and we multiply by three so we can support triplets of notes.

## Token Schema

The model is trained on tokenized midi files, composed of a series of ***messages***, which are composed of ***tokens***. Here is a list of the types of tokens:

1. A ***control*** token is a word like `STEP`, `NOTE`, `PAD`, etc.
2. A ***pitch*** token is the character `P` followed by the pitch as a number. `P60` represents Middle C, `P61` represents C Sharp, `P62` represents "Middle" D, `P72` represents C5.
3. A ***duration*** token is `D` followed by the duration in ticks as a number.
4. A ***ticks*** token is `T` followed by the number of ticks as a number.
5. *A **beat** token was supported in older versions of the model, represented as a `B` followed by a number.*
6. Time signature and tempo tokens will be elaborated on in their respective messages.

We assume that there will be 12 ticks per beat. One beat will typically be a quarter note.

### Pad Message

Used for padding content when feeding the model seed tokens. Consists of one control token...

```
PAD
```

### Time Signature Message

Typically found at the start of a tokenized song. Represents a change in the time signature. Consists of the time signature control token along with the specified time signature in the form `TS.{n}.{d}` where `n` is the numerator and `d` is the denominator.

As of now, only 4/4, 3/4, and 6/8 are supported.

```
TIMESIG TS.4.4
```

### Tempo Message

Typically found at the start of a tokenized song. Represents a change in the tempo. Consists of a tempo marking.

```
TEMPO ALLEGRO
```

### Note Message

Used to specified that a note is being played at the current time index.

Consists of the `NOTE` control token, along with a duration and pitch.

This represents Middle C played for a beat...

```
NOTE D12 P60
```

### Step Message

Used to increment time.

Consists of the `STEP` control token, along with the number of ticks to increment time by.

This represents incrementing time by two beats (twenty-four ticks)...

```
STEP T24
```

### End of Song Message

Consists of the end of song control token.

```
END
```