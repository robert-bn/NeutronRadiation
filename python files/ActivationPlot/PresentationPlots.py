from numpy import linspace
import ActivationPlot as ap

ap.make_plot(
    fileName="water_HADROTHE.json",
#    title="Activation of water phantom immediately after beam turned off",
    outName="water_HADROTHE_high_act.pdf",
    outDir="presentationpdfs/",
    exclude=["Be7", "F18", "F17"],
    ymin=1e4,
    ymax=4e7,
    bbox=(0., 0.5, 0.5, 0.5),
    xlim=(20,250),
    fig_size=(12,6.75)
)


ap.make_plot(
    fileName="water_HADROTHE.json",
#    title="Activation of water phantom immediately after beam turned off",
    outName="water_HADROTHE_low_act.pdf",
    outDir="presentationpdfs/",
    include_only=["Be7", "F18"],
    ymin=1,
    ymax=2e2,
    bbox=(0.75, 0., 0.25, 0.4),
    xlim=(20,250),
    fig_size=(12,6.75)
)


ap.make_plot(
    fileName="rangeshifter_t1_HADROTHE.json",
#    title="Activation of water phantom immediately after beam turned off",
    outName="rangeshifter_t1_HADROTHE_high_act.pdf",
    outDir="presentationpdfs/",
    exclude=["Be7", "F18", "F17", "C15"],
    ymin=9e1,
    ymax=5e5,
    xlim=(70,250),
    fig_size=(12,6.75)
)

ap.make_plot(
    fileName="rangeshifter_t1_HADROTHE.json",
#    title="Activation of water phantom immediately after beam turned off",
    outName="rangeshifter_t1_HADROTHE_low_act.pdf",
    outDir="presentationpdfs/",
    include_only=["Be7"],
    ymin=1e1,
    ymax=2e1,
    yticks=linspace(1e1,2e1,9),
    xlim=(70,250),
    fig_size=(12,6.75)
)
