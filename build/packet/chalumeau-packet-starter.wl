(* Chalumeau family acoustic starter - generated 2026-05-03 *)

ClearAll["Global`*"];

speedOfSoundInPerSec = 13552.0;
midiFrequency[m_] := 440*2^((m - 69)/12);
centsError[measured_, target_] := 1200*Log2[measured/target];

bodyLength[rootMidi_, boreID_] := Module[
  {f = midiFrequency[rootMidi], acoustic, bellCorr, reedCorr},
  acoustic = speedOfSoundInPerSec/(4*f);
  bellCorr = 0.61*(boreID/2);
  reedCorr = 0.25*boreID;
  acoustic - bellCorr - reedCorr
];

holeXFromBell[rootMidi_, offset_, boreID_, holeRatio_] := Module[
  {f = midiFrequency[rootMidi + offset], holeDia, holeCorr, reedCorr, eff, body},
  holeDia = boreID*holeRatio;
  holeCorr = 0.30*holeDia;
  reedCorr = 0.25*boreID;
  eff = speedOfSoundInPerSec/(4*f);
  body = bodyLength[rootMidi, boreID];
  body - (eff - reedCorr - holeCorr)
];

variants = {
  <|"ID" -> "CLM-SOP-C4", "RootMIDI" -> 60, "BoreID" -> 0.500|>,
  <|"ID" -> "CLM-ALT-G3", "RootMIDI" -> 55, "BoreID" -> 0.625|>,
  <|"ID" -> "CLM-TEN-C3", "RootMIDI" -> 48, "BoreID" -> 0.750|>,
  <|"ID" -> "CLM-BAS-F2", "RootMIDI" -> 41, "BoreID" -> 0.875|>
};

holeOffsets = {1, 2, 4, 5, 7, 9, 10, 11, 12};
holeRatios = {0.32, 0.36, 0.38, 0.34, 0.38, 0.40, 0.30, 0.34, 0.32};

familyTable = Table[
  With[{v = variants[[i]]},
    <|
      "ID" -> v["ID"],
      "RootHz" -> midiFrequency[v["RootMIDI"]],
      "BodyLengthIn" -> bodyLength[v["RootMIDI"], v["BoreID"]],
      "HolePositionsFromBellIn" -> MapThread[
holeXFromBell[v["RootMIDI"], #1, v["BoreID"], #2]&,
{holeOffsets, holeRatios}
      ]
    |>
  ],
  {i, Length[variants]}
];

Dataset[familyTable]

Manipulate[
  Plot[
    speedOfSoundInPerSec/(4*(x + 0.61*(bore/2) + 0.25*bore)),
    {x, 4, 42},
    PlotRange -> {80, 700},
    AxesLabel -> {"Body length (in)", "Frequency (Hz)"},
    PlotLabel -> "Stopped cylindrical reed bore first-pass model"
  ],
  {{bore, 0.5, "Bore ID (in)"}, 0.35, 1.0}
]
