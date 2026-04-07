import datetime
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class CandleChart:
    date_list = []
    DATE_FORMAT_YMD = "%Y-%m-%d"
    graph_margin = {"l": 20, "r": 20, "t": 20, "b": 20}
    setting_dict = {
        "chart": 1.0,
        # "chart2": 0.5,
        "volume": 0.1,
        "RSI 6/14": 0.3,
        "TSI": 0.3,
        "DE": 0.3,
        "FIREHILL": 0.2,
        "MCD": 0.2
    }

    @staticmethod
    def initilize_date_list(index):
        if isinstance(type(index[0]), str):
            start_date = datetime.datetime.strptime(index[0], CandleChart.DATE_FORMAT_YMD)
        else:
            start_date = index[0]

        while start_date < index[-1]:
            if (start_date.strftime(CandleChart.DATE_FORMAT_YMD) not in index):
                CandleChart.date_list.append(start_date.strftime(CandleChart.DATE_FORMAT_YMD))
            start_date += datetime.timedelta(days=1)

    def __init__(self, data: pd.DataFrame, name: str, h_line_list = []):
        self.data = data
        self.h_line_list = h_line_list
        if len(CandleChart.date_list) == 0:
            data_index = data.index
            if type(data_index[0]) == str:
                data_index = data_index.map(lambda x: datetime.datetime.strptime(x, CandleChart.DATE_FORMAT_YMD))
            CandleChart.initilize_date_list(data_index)
        self.titles = ['chart', 'volume']
        if 'rsi6' in data.columns and 'rsi14' in data.columns:
            self.titles.append('RSI 6/14')
        if 'tsi' in data.columns:
            self.titles.append('TSI')
        if 'de' in data.columns:
            self.titles.append('DE')
        if 'buyer' in data.columns:
            self.titles.append('FIREHILL')
        if 'mm_rsi' in data.columns:
            self.titles.append('MCD')
        self.titles = tuple(self.titles)
        self.width  = [CandleChart.setting_dict[title] for title in self.titles]
        self.width.reverse()
        self.hhv    = self.data['High'].max()
        self.llv    = self.data['Low'].min()
        self.name   = name

        if len(self.titles) != len(self.width):
            print("ERROR, titles != width")

    def plot(self):
        fig = make_subplots(rows=len(self.titles), cols=1, shared_xaxes=True,
                            vertical_spacing=0.02, subplot_titles=self.titles,
                            row_width=self.width)

        self.row = 1

        fig.add_trace(go.Candlestick(
            x=self.data['Date'],
            open=self.data['Open'],
            high=self.data['High'],
            low=self.data['Low'],
            close=self.data['Close'],
            showlegend=False,
            name=self.name
        ), row=self.row, col=1)

        main_plot_list = [
            ["ema11", "#FF97FF", "EMA11", True],
            ["ema25", "#FECB52", "EMA25", True],
            ["ema48", "#66AA00", "EMA48", True],
            ["ema200", "purple", "EMA200", True],
            ["bb_bbh", "blue", "BBH", False],
            ["bb_bbm", "blue", "BBM", False],
            ["bb_bbl", "blue", "BBL", False],
            ["super_bbh", "#B6E880", "SBBH", False],
            ["super_bbm", "green", "SBBM", False],
            ["super_bbl", "#B6E880", "SBBL", False],
        ]

        main_plot_list = [item for item in main_plot_list if item[0] in self.data.columns]
        for item in main_plot_list:
            fig.add_trace(go.Scatter(
            x=self.data.index, y=self.data[item[0]], line=go.scatter.Line(color=item[1]), showlegend=item[3], name=item[2]), row=self.row, col=1)

        self.row += 1
        positive_data = self.data[self.data["Close"] >= self.data["Open"]]
        negative_data = self.data[self.data["Close"] < self.data["Open"]]
        
        fig.add_trace(go.Bar(
            x=positive_data.index, y=positive_data['Volume'],
            showlegend=False, marker_color="green"),
            row=self.row, col=1)
        fig.add_trace(go.Bar(
            x=negative_data.index, y=negative_data['Volume'],
            showlegend=False, marker_color="red"),
            row=self.row, col=1)
        if "Volume_ma5" in self.data.columns:
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data["Volume_ma5"], line=go.scatter.Line(color="black"), showlegend=False), row=self.row, col=1)

        if "RSI 6/14" in self.titles:
            self.row += 1
            rsi_line_list = [
                ["rsi6", "red", "RSI6"],
                ["rsi14", "green", "RSI14"],
            ]
            for item in rsi_line_list:
                fig.add_trace(go.Scatter(x=self.data.index, y=self.data[item[0]], line=go.scatter.Line(color=item[1]), showlegend=False, name=item[2]), row=self.row, col=1)
            if "rsi14_ma14" in self.data.columns:
                fig.add_trace(go.Scatter(x=self.data.index, y=self.data["rsi14_ma14"], line=go.scatter.Line(color="purple"), showlegend=False, name="RSI14_MA14"), row=self.row, col=1)

            fig.add_hline(y=30, line_color="black", row=self.row, col=1)
            fig.add_hline(y=70, line_color="black", row=self.row, col=1)
        
        if "TSI" in self.titles:
            self.row += 1
            tsi_line_list = [
                ["tsi", "blue", "TSI"],
                ["tsi_smooth", "red", "TSI_SMOOTH"],
            ]
            for item in tsi_line_list:
                fig.add_trace(go.Scatter(x=self.data.index, y=self.data[item[0]], line=go.scatter.Line(color=item[1]), showlegend=False, name=item[2]), row=self.row, col=1)

        if "DE" in self.titles:
            self.row += 1
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['de'], line=go.scatter.Line(color="black"), showlegend=False), row=self.row, col=1)
            fig.add_hline(y=0, line_color="black", row=self.row, col=1)
            positive_de_data = self.data[self.data["de_change"] >= 0]
            negative_de_data = self.data[self.data["de_change"] <= 0]
            fig.add_trace(go.Bar(
                x=positive_de_data.index, y=positive_de_data['de'],
                showlegend=False, marker_color="green"),
                row=self.row, col=1)
            fig.add_trace(go.Bar(
                x=negative_de_data.index, y=negative_de_data['de'],
                showlegend=False, marker_color="red"),
                row=self.row, col=1)
            
        if "FIREHILL" in self.titles:
            self.row += 1
            firehill_line_list = [
                ["market_maker", "red", ""],
                ["retail", "green", ""],
            ]
            for item in firehill_line_list:
                fig.add_trace(go.Scatter(x=self.data.index, y=self.data[item[0]], line=go.scatter.Line(color=item[1]), showlegend=False, name=item[2]), row=self.row, col=1)
            fig.add_trace(go.Bar(x=self.data.index, y=self.data['buyer'], showlegend=False), row=self.row, col=1)

        if "MCD" in self.titles:
            self.row += 1
            mcd_line_list = [
                ["hot_rsi", "yellow", ""],
                ["mm_rsi", "red", ""],
            ]
            fig.add_trace(go.Bar(x=self.data.index, y=[20 for _ in range(self.data.shape[0])], showlegend=False, marker_color="green"), row=self.row, col=1)
            for item in mcd_line_list:
                fig.add_trace(go.Bar(x=self.data.index, y=self.data[item[0]],showlegend=False, marker_color=item[1]), row=self.row, col=1)
        
        zz_shapes = list(fig.layout.shapes)
        zz_annotations = list(fig.layout.annotations)
        for annotation in zz_annotations:
            annotation.font.size = 12

        
        fig.update_layout(margin=CandleChart.graph_margin,
                          yaxis2 = dict(range=[self.data["Close"].iloc[-40:0].min() * 0.9, self.data["Close"].iloc[-40:0].max() * 1.1]),
                          paper_bgcolor="LightGray",
                          legend={
                              "orientation": "h",
                              "yanchor": "bottom",
                              "y": 1.02,
                              "xanchor": "right",
                              "x": 1
                          },
                          shapes=zz_shapes,
                          annotations=zz_annotations,
                          height=sum(self.width)*400,
                          barmode="overlay")

        tick_vals = fig.data[0]['x'][::39]
        tick_text = [i.strftime(CandleChart.DATE_FORMAT_YMD) for i in tick_vals]
        fig.update_xaxes(
            rangeslider_visible=False,
            tickvals=fig.data[0]['x'][::39],
            ticktext=tick_text,
        )
        fig.for_each_xaxis(lambda ax: ax.update(type='category'))

        self.fig = fig

    def get_chart_as_bytes(self, format="png"):
        img_bytes = self.fig.to_image(format=format)
        return img_bytes

    def save_chart(self, name: str):
        if os.path.exists(f"/home/user/Documents/stock_html/resources"):
            self.fig.write_image(f"/home/user/Documents/stock_html/resources/{name}.png")