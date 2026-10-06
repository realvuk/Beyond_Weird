"""Improve Figure 2 typography without changing its scores or panels."""
from pathlib import Path
import sys
ROOT=Path('/Users/vuk/Downloads/BWEIRD')
sys.path.insert(0,str(ROOT/'figures'))
from reproduce import load_results
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

names,w,s,pooled,per_model=load_results(ROOT)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,
                     'axes.spines.top':False,'axes.spines.right':False,
                     'pdf.fonttype':42})
fig=plt.figure(figsize=(10.5,9.0),layout='constrained')
grid=fig.add_gridspec(2,2,height_ratios=[1.1,1],width_ratios=[1,1.45])
axes=[fig.add_subplot(grid[0,0]),fig.add_subplot(grid[0,1]),fig.add_subplot(grid[1,:])]
for ax,wa,sa,labels,title in [
    (axes[0],w.mean(axis=0),s.mean(axis=0),[f'Pair {p}' for p in range(1,9)],'A. Eight topic-pair means'),
    (axes[1],w.mean(axis=1),s.mean(axis=1),names,'B. Thirteen model means')]:
    y=np.arange(len(labels))
    ax.hlines(y,np.minimum(wa,sa),np.maximum(wa,sa),color='#b4bdc5',lw=2)
    ax.scatter(wa,y,color='#225e91',s=35,label='WEIRD',zorder=3)
    ax.scatter(sa,y,color='#b95832',s=35,label='Serbian',zorder=3)
    ax.set(yticks=y,yticklabels=labels,xlim=(0,1),xlabel='Recall',title=title)
    ax.invert_yaxis()
    ax.grid(axis='x',alpha=.15)
axes[0].legend(loc='lower left',frameon=False,fontsize=10)
axes[2].scatter(s.ravel(),w.ravel(),s=28,alpha=.6,color='#225e91',edgecolor='none')
axes[2].plot([0,1],[0,1],color='#7c8994',ls='--',lw=1)
axes[2].set(xlim=(0,1),ylim=(0,1),xlabel='Serbian recall',ylabel='WEIRD recall',
            title='C. All 104 matched cells',aspect='equal')
# Caption carries the weighting/dependence statement at manuscript text size.
out=Path(__file__).resolve().parent/'manuscript/plots'
fig.savefig(out/'paired_recall.pdf',bbox_inches='tight',metadata={'CreationDate':None,'ModDate':None})
fig.savefig(out/'paired_recall.png',bbox_inches='tight',dpi=180)
assert w.shape == s.shape == (13,8)
assert len(axes[2].collections[0].get_offsets()) == 104
print('Figure 2: unchanged 104 cells; larger vector labels in a two-row layout.')
