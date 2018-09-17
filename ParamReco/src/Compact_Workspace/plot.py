# Abe Tishelman-Charny
# 20 July 2018
# The purpose of this program is to plot average bias vs. time shift for multiple 

# https://www-zeuthen.desy.de/~middell/public/pyroot/pyroot.html

from ROOT import *
from array import array
import os
import argparse

# dashed line across zero? 

parser = argparse.ArgumentParser(description='Process some files')
#parser.add_argument('-f', '--files', type = str, nargs='+' , help='files to plot from')
parser.add_argument('-d', '--directory', type = str, nargs='+',  help='directory to root files')
parser.add_argument('-t', '--plot_type', type = str, nargs='+',  help='Type of Plot, BC or EC')
args = parser.parse_args()

# Open all flies from desired directory

paths = []
data_folder = args.directory[0]
plot_type = str(args.plot_type[0]) # BC or EC

print "plot type = ",plot_type

# Find all files in current working directory ending in ".root"
# for data_folder path in current directory
for file in os.listdir(str(os.getcwd()) + '/' + str(data_folder)):
    if file.endswith(".root"):
        print(os.path.join(file))
	paths.append(str(data_folder) + '/' + os.path.join(file))

print "paths = ",paths

print "len(paths) = ",len(paths)

#elem0 = paths[0]
#elem1 = paths[1]

#paths[0] = elem1
#paths[1] = elem0

gStyle.SetOptStat(0); # no stats box

# figure out how to loop 
# Set maximum number of files 
f1 = TFile()
f2 = TFile()
f3 = TFile()
f4 = TFile() 
f5 = TFile()
f6 = TFile()

h1 = TH1F()
h2 = TH1F()
h3 = TH1F()
h4 = TH1F()
h5 = TH1F()
h6 = TH1F()

g1 = TGraph()
g2 = TGraph()
g3 = TGraph()
g4 = TGraph()
g5 = TGraph()
g6 = TGraph()

files = [f1, f2, f3, f4, f5, f6]
histos = [h1, h2, h3, h4, h5, h6]
graphs = [g1, g2, g3, g4, g5, g6]

i = 0

for path in paths: # Should start with this and create 
	files[i] = TFile.Open(paths[i])
	if plot_type == 'EC':
		histos[i] = files[i].Get("EC")
	elif plot_type == 'BC':
		histos[i] = files[i].Get("tsr")
	i += 1
	#files.append()	
	#f1 = TFile.Open(path) 

extra = len(histos) - len(paths)

while extra > 0:
	files = files[:-1]
	histos = histos[:-1]
	graphs = graphs[:-1]
	extra -= 1

# Doing the following because g = TGraph(h) seems to incorrectly translate values. 

abs_val = False

for h, hist in enumerate(histos, 1): 

	counter = 1
	value = 0
	ts = 0
	dt = hist.GetXaxis().GetBinLowEdge(3) - hist.GetXaxis().GetBinLowEdge(2)

	x = array('d')
	y = array('d')

	#print'x = ',x
	#print'y = ',y

	while(hist.GetBinContent(counter) != 0):
		#print ("hist.GetXaxis().GetBinContent(" + str(counter) + ") = " + str(hist.GetXaxis().GetBinLowEdge(counter)))
		ts = hist.GetXaxis().GetBinLowEdge(counter)
		#print ("hist.GetBinContent(" + str(counter) + ") = " + str(hist.GetBinContent(counter)))
		value = hist.GetBinContent(counter)

		#cout << "abs(" << value << ") = " << abs(value) << endl;
		#h2->Fill(ts,fabs(value));
		x.append(ts)
		if (abs_val): y.append(fabs(value))
		else: y.append(value)
		print("ts = " + str(ts) )
		print("value = " + str(value) )
		print("counter = " + str(counter) )
		ts += dt
		counter += 1

	#graphs[h - 1] = TGraph(counter - 1, x, y)
	graphs[h - 1] = TGraph(counter - 1,x,y)

i = 0

# Read weight type and year 

# paths[i].split('_')[-4] # weights type
# paths[i].split('_')[-3] # year

if plot_type == 'BC':
	for g in graphs:
		g.SetMarkerStyle(8)

		if paths[i].split('_')[-4] == "online": 
			if paths[i].split('_')[-3] == "2017":
				g.SetMarkerColor(kRed + 2) 
				g.SetLineColor(kRed + 2)
			elif paths[i].split('_')[-3] == "2018":
				g.SetMarkerColor(kRed) 
				g.SetLineColor(kRed)

		if paths[i].split('_')[-4] == "PedSub1+4": 
			if paths[i].split('_')[-3] == "2017":
				print 'year = 2017'
				g.SetMarkerColor(kGreen + 4) 
				g.SetLineColor(kGreen + 4)
			elif paths[i].split('_')[-3] == "2018":
				print 'year = 2018'
				g.SetMarkerColor(kGreen) 
				g.SetLineColor(kGreen)
		i += 1

elif plot_type == 'EC':
	for g in graphs:
		min_eta = paths[i].split('_')[-7] #when there's a note. With no note, one less '_'
		max_eta = paths[i].split('_')[-6]
		g.SetMarkerStyle(8)

		if (min_eta == 0) and (max_eta == 1.4):
				g.SetMarkerColor(kRed) 
				g.SetLineColor(kRed)

		if (min_eta == 1.4) and (max_eta == 1.8):
				g.SetMarkerColor(kGreen) 
				g.SetLineColor(kGreen)

		if (min_eta == 1.8) and (max_eta == 2.1):
				g.SetMarkerColor(kBlue) 
				g.SetLineColor(kBlue)

		if (min_eta == 2.1) and (max_eta == 2.4):
				g.SetMarkerColor(kPink) 
				g.SetLineColor(kPink)

		if (min_eta == 2.4) and (max_eta == 2.7):
				g.SetMarkerColor(kCyan) 
				g.SetLineColor(kCyan)

		if (min_eta == 2.7) and (max_eta == 3):
				g.SetMarkerColor(kOrange) 
				g.SetLineColor(kOrange)
		i += 1
	#g.SetMarkerColor(2+i)
	#g.SetLineColor(2+i)
	#i += 1	

#graphs[0].SetMarkerColor(kBlue)
#graphs[0].SetLineColor(kBlue)

#graphs[1].SetMarkerColor(kGreen)
#graphs[1].SetLineColor(kGreen)

#graphs[2].SetMarkerColor(kRed)
#graphs[2].SetLineColor(kRed)



#g1.SetMarkerStyle(8)
#g1.SetMarkerColor(3)
#g1.SetLineColor(3)

#if(abs_val) g1->SetTitle("EB abs(Average Bias) vs. Time Shift")
#else g1->SetTitle("EB Average Bias vs. Time Shift");
#g1->GetXaxis()->SetTitle("Time Shift (ns)");
#g1->GetXaxis()->SetTitleOffset(1.3);
#if(abs_val) g1->GetYaxis()->SetTitle("abs(Average Bias)");
#else g1->GetYaxis()->SetTitle("Average Bias");
#g1->GetYaxis()->SetTitleOffset(1.5);

#g1->Draw();
i = 0
for g in graphs:
	g.SetName("g" + str(i))
	i += 1

#if (abs_val): l1 = TLegend(0.5, 0.5, 0.8, 0.8)
#else: l1 = TLegend(0.7, 0.1, 0.9, 0.3)
#else: l1 = TLegend(0.5, 0.1, 0.8, 0.4)

l1 = TLegend(0.7, 0.1, 0.9, 0.3) # Bottom right
#l1 = TLegend(0.1, 0.7, 0.3, 0.9) # Upper left

#l1.SetHeader("Legend") # I actually can't believe you can declare l1 in an if statement then access outside 

i = 0

for g in graphs:
	label = paths[i].split('_')[-4] + '_' + paths[i].split('_')[-3]
	l1.AddEntry(g, label, "lp")
	i += 1

#paths[0].slice('_')[1] # section_weights_range.root
#section = str(paths[0])[10:-17] # EE+/-, EB
#section = paths[0].split('_')[-3].split('/')[-1]
section = paths[0].split('_')[-5] #.split('/')[-1]
minimum = paths[0].split('_')[-2] + 'ns'
maximum = paths[0].split('.')[-2].split('_')[-1] + 'ns'

print 'section = ',section

mg = TMultiGraph()

for g in graphs:
	mg.Add(g, "LP")

mg.SetTitle(section + " Average Bias vs. Time Shift")

c0 = TCanvas('c0', 'c0', 800, 600)
c0.SetBatch(kTRUE)

mg.Draw("A")
mg.GetXaxis().SetTitle("Time Shift (ns)")
#mg.GetXaxis().SetRangeUser(-3,3)
#mg.GetYaxis().SetRangeUser(-0.04,0.02)
mg.GetYaxis().SetTitle("Average Bias")
mg.GetYaxis().SetTitleOffset(1.3)


xline = TLine(c0.GetUxmin(),0,c0.GetUxmax(),0)
#xline = TLine(-3,0,3,0)
xline.SetLineColor(kBlack)
xline.SetLineStyle(1)

yline = TLine(0,c0.GetUymin(),0,c0.GetUymax())
#yline = TLine(0,-0.04,0,0.02)
yline.SetLineColor(kBlack)
yline.SetLineStyle(1)

l1.Draw("SAME")
xline.Draw("SAME")
yline.Draw("SAME")

#Save_Title = "plots/plot" + section + str(int(histos[0].GetXaxis().GetBinLowEdge(1))) + ".pdf"
#Save_Title = "bin/pyplot" + section + "_" + str(int(histos[0].GetXaxis().GetBinLowEdge(1))) + ".pdf"
Save_Title = "bin/pyplot" + section + "_" + minimum + '_' + maximum + ".pdf"

c0.SaveAs(Save_Title)