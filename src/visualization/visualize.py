import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import io

def barv_npsmean_by(dataframe, axisX):
    buf = io.BytesIO()

    # Converter NPS interno para número
    dataframe["NPS interno"] = pd.to_numeric(dataframe["NPS interno"], errors='coerce')
    dataframe = dataframe.dropna(subset=["NPS interno"])

    # Agrupar explicitamente só pela coluna NPS interno
    grouped = dataframe.groupby([f"{axisX}"])[["NPS interno"]].mean()

    axisX_labels = grouped.index
    nps_mean_by_axisX = grouped["NPS interno"].values

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(axisX_labels, nps_mean_by_axisX)
    ax.set_ylabel("NPS interno mensal médio")
    ax.set_yticks(np.array(range(0, 11, 1)))
    ax.set_title(f"Média de NPS Interno Mensal por {axisX}")
    fig.savefig(buf, format='png')
    plt.close(fig)
    return buf

def hist_nps(dataframe):
    buf = io.BytesIO()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(dataframe["NPS interno"])
    ax.set_title("Distribuição do NPS interno mensal")
    ax.set_xlabel("Nps Interno")
    fig.savefig(buf, format='png')
    plt.close(fig)
    return buf