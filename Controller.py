from Frame import Frame
from KSTest import KSTest
from MeanTest import MeanTest
from VarianceTest import VarianceTest
from Chi2Test import Chi2Test
from PokerTest import PokerTest
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.stats import *
from statsmodels.distributions.empirical_distribution import ECDF
import tkinter as tk

class Controller:
    def __init__(self):
        self.fr = Frame(self)
        self.meanTest = MeanTest()
        self.varTest = VarianceTest()
        self.chi2 = Chi2Test()
        self.ks = KSTest()
        self.poker = PokerTest()
        self.fig = plt.figure(figsize=(5, 3),dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master= self.fr.mywindow)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT)
        self.fr.mywindow.mainloop()

    """It grabs the data from the given file path""" 
    def getDataFromFile(self, filename):
        df = pd.read_csv(filename, header=None) if filename.endswith('.csv') else pd.read_excel(filename, header=None)
        arr = np.array(df)
        non_null_arr = arr[~np.isnan(arr)]
        return non_null_arr
    
    """Main method to do all tests"""
    def makeTest(self):
        data =self.getDataFromFile(self.fr.getFilePath())
        option = self.fr.getSelectedOption()
        print(data)
        if option == 'Mean Test':
            self.fr.destroyAlllbls() # Destroy previous labels
            self.fr.generateLbl("MEAN TEST")
            #Make the test
            nums,freqs,n =self.meanTest.evaluate(data)
            #Shows information
            self.fr.generateLbl(f"Number of samples: {n}")
            self.fr.generateLbl(f"Approved Numbers: {nums}",40)
            self.fr.generateLbl(f"Frequencies: {freqs}")
            self.drawMeanFigure(data) #Finally paint the graphic
            self.fr.generateLblToDescribeGraph("With this graph you can see if the data follow a normal distribution and if the sample mean is significantly different from the population mean.")
        elif option == 'Variance Test':
            self.fr.destroyAlllbls() # Destroy previous labels
            self.fr.generateLbl("VARIANCE TEST")
            #Make the test
            valid, n,nums,li,ls= self.varTest.evaluate(data)
            #Shows information
            self.fr.generateLbl(f"Number of samples: {n}")
            self.fr.generateLbl(f"Passed test: {valid}")
            self.fr.generateLbl(f"Approved Numbers: {nums}")
            self.fr.generateLbl(f"LI: {li}")
            self.fr.generateLbl(f"LS: {ls}")
            self.drawVarFigure(data) #Finally paint the graphic
            self.fr.generateLblToDescribeGraph("If the variances are similar, the boxes should be approximately the same size. If the variances are different, the box of the distribution with the largest variance will be larger.")
        elif option == 'KS Test':
            self.fr.destroyAlllbls() # Destroy previous labels
            self.fr.generateLbl("KS TEST")
            #Make the test
            n,valid,dif, ksvalue=self.ks.evaluate(data) # Evaluate
            #Shows information
            self.fr.generateLbl(f"Number of samples: {n}")
            self.fr.generateLbl(f"Passed test: {valid}")
            self.fr.generateLbl(f"Max Difference: {dif}")
            self.fr.generateLbl(f"KSValue associated: {ksvalue}")
            self.drawKSFigure(data) #Finally paint the graphic
            self.fr.generateLblToDescribeGraph("A cumulative distribution function (CDF) of the data was plotted and compared to the CDF of the theoretical distribution. In this way, it is possible to visualize if the data follow the theoretical distribution or not.")
        elif option == 'Chi2 Test':
            self.fr.destroyAlllbls() # Destroy previous labels
            self.fr.generateLbl("CHI2 TEST")
            #Make the test
            statistic, chi_value, obs_freq, expect_freq, bin_edges, status_hypo,n =self.chi2.evaluate(data)
            #Shows information
            self.fr.generateLbl(f"Number of samples: {n}")
            self.fr.generateLbl(f"Status: {status_hypo}")
            self.fr.generateLbl(f"Observed frequency: {obs_freq}")
            self.fr.generateLbl(f"Expected frequency: {expect_freq}")
            self.fr.generateLbl(f"Obtained Value: {statistic}")
            self.fr.generateLbl(f"Chi2Value Associated: {chi_value}")
            self.drawChi2Figure(data) #Finally paint the graphic
            self.fr.generateLblToDescribeGraph("For this plot, the expected frequency for each histogram interval was calculated and compared to the observed frequency. If there is a large difference between the expected and observed frequencies, it can be concluded that the data does not follow the theoretical distribution.")
        elif option == 'Poker Test':
            self.fr.destroyAlllbls() # Destroy previous labels
            self.fr.generateLbl("POKER TEST")
            #Make the test
            statistics, counts, value,n, Oi,Ei=self.poker.evaluate(data)
            #Shows information
            self.fr.generateLbl(f"Number of samples: {n}")
            self.fr.generateLbl(f"Obtained Value: {value}")
            self.fr.generateLbl(f"Poker counts: {counts}")
            self.fr.generateLbl(f"PokerValue Associated: {statistics}")
            self.drawPokerFigure(data,Oi,Ei) #Finally paint the graphic
            self.fr.generateLblToDescribeGraph("For this graph, we compare the expected frequencies of each hand, with the theoretical frequencies according to the poker test, so we can see which hands the sample tended to drop the most.")
        else: 
            pass
    

    def drawMeanFigure(self,data):
        mu, sigma = self.meanTest.getMeanAndStd()
        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        ax = self.fig.add_subplot(111)
        ax.hist(data, density=True, alpha=0.5)
        xmin, xmax = ax.get_xlim()
        # Generate x-values ​​for the normal distribution
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, sigma)
        # Graph the normal distribution
        ax.plot(x, p, 'k', linewidth=2)
        ax.set_title("Mean Test")
        self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.fig, master= self.fr.mywindow)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT)
        # Update the window with the new figure
        self.fr.mywindow.update()

    def drawVarFigure(self,data):
        self.fig.clear()
        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        ax = self.fig.add_subplot(111)
        ax.set_title("Variance Test")
        ax.boxplot(data)
        self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.fig, master= self.fr.mywindow)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT)
        # Update the window with the new figure
        self.fr.mywindow.update()
    
    def drawKSFigure(self,data):
        self.fig.clear()
        self.fig = plt.figure(figsize=(5, 3))
        ax = self.fig.add_subplot(111)
        mu, sigma= self.ks.getMeanAndStd(data)
        x = np.linspace(norm.ppf(0.01), norm.ppf(0.99), 100)
        # pdf = norm.pdf(x, mu, sigma)
        cdf = norm.cdf(x, mu, sigma)
        e_cdf = ECDF(data)
        ax.set_title("KS Test")
        ax.plot(e_cdf.x, e_cdf.y, label='Empirical CDF')
        ax.plot(x, cdf, label='Theoretical CDF')

        self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.fig, master= self.fr.mywindow)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT)
        # Update the window with the new figure
        self.fr.mywindow.update()
    
    def drawChi2Figure(self,data):
        self.fig.clear()
        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        ax = self.fig.add_subplot(111)
        mu, sigma = self.chi2.getMeanAndStd(data)
        n_bins = int(1 + np.log2(len(data)))
        bins = np.histogram_bin_edges(data, bins=n_bins)
        # Calculate the observed frequencies
        observed, _ = np.histogram(data, bins=bins)

        # Calculate the expected frequencies using the normal distribution
        expected = len(data) * np.diff(norm.cdf(bins, mu, sigma))

        # Plot the histogram and compare the observed and expected frequencies
        ax.set_title("Chi2 Test")
        ax.hist(data, bins=bins, alpha=0.5, label='Observed') 
        ax.plot(bins[1:], expected, label='Expected')
        self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.fig, master= self.fr.mywindow)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT)
        # Update the window with the new figure
        self.fr.mywindow.update()

    def drawPokerFigure(self,data, Oi,Ei):
        self.fig.clear()
        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        ax = self.fig.add_subplot(111)
        tags = ["D","0","T","K","F","P","Q"] # tags for every hand of poker
        ax.set_title("Poker Test")
        ax.bar(tags, Oi, label="Frecuencia observada")
        ax.plot(tags, Ei, label="Frecuencia esperada")
        self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.fig, master= self.fr.mywindow)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT)
        # Update the window with the new figure
        self.fr.mywindow.update()

if __name__ == "__main__":
    control = Controller()