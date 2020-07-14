
<!DOCTYPE html
  PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
   <!--
This HTML was auto-generated from MATLAB code.
To make changes, update the MATLAB code and republish this document.
      --><title>new_pepper_pot</title><meta name="generator" content="MATLAB 9.8"><link rel="schema.DC" href="http://purl.org/dc/elements/1.1/"><meta name="DC.date" content="2020-06-25"><meta name="DC.source" content="new_pepper_pot.m"><style type="text/css">
html,body,div,span,applet,object,iframe,h1,h2,h3,h4,h5,h6,p,blockquote,pre,a,abbr,acronym,address,big,cite,code,del,dfn,em,font,img,ins,kbd,q,s,samp,small,strike,strong,sub,sup,tt,var,b,u,i,center,dl,dt,dd,ol,ul,li,fieldset,form,label,legend,table,caption,tbody,tfoot,thead,tr,th,td{margin:0;padding:0;border:0;outline:0;font-size:100%;vertical-align:baseline;background:transparent}body{line-height:1}ol,ul{list-style:none}blockquote,q{quotes:none}blockquote:before,blockquote:after,q:before,q:after{content:'';content:none}:focus{outine:0}ins{text-decoration:none}del{text-decoration:line-through}table{border-collapse:collapse;border-spacing:0}

html { min-height:100%; margin-bottom:1px; }
html body { height:100%; margin:0px; font-family:Arial, Helvetica, sans-serif; font-size:10px; color:#000; line-height:140%; background:#fff none; overflow-y:scroll; }
html body td { vertical-align:top; text-align:left; }

h1 { padding:0px; margin:0px 0px 25px; font-family:Arial, Helvetica, sans-serif; font-size:1.5em; color:#d55000; line-height:100%; font-weight:normal; }
h2 { padding:0px; margin:0px 0px 8px; font-family:Arial, Helvetica, sans-serif; font-size:1.2em; color:#000; font-weight:bold; line-height:140%; border-bottom:1px solid #d6d4d4; display:block; }
h3 { padding:0px; margin:0px 0px 5px; font-family:Arial, Helvetica, sans-serif; font-size:1.1em; color:#000; font-weight:bold; line-height:140%; }

a { color:#005fce; text-decoration:none; }
a:hover { color:#005fce; text-decoration:underline; }
a:visited { color:#004aa0; text-decoration:none; }

p { padding:0px; margin:0px 0px 20px; }
img { padding:0px; margin:0px 0px 20px; border:none; }
p img, pre img, tt img, li img, h1 img, h2 img { margin-bottom:0px; }

ul { padding:0px; margin:0px 0px 20px 23px; list-style:square; }
ul li { padding:0px; margin:0px 0px 7px 0px; }
ul li ul { padding:5px 0px 0px; margin:0px 0px 7px 23px; }
ul li ol li { list-style:decimal; }
ol { padding:0px; margin:0px 0px 20px 0px; list-style:decimal; }
ol li { padding:0px; margin:0px 0px 7px 23px; list-style-type:decimal; }
ol li ol { padding:5px 0px 0px; margin:0px 0px 7px 0px; }
ol li ol li { list-style-type:lower-alpha; }
ol li ul { padding-top:7px; }
ol li ul li { list-style:square; }

.content { font-size:1.2em; line-height:140%; padding: 20px; }

pre, code { font-size:12px; }
tt { font-size: 1.2em; }
pre { margin:0px 0px 20px; }
pre.codeinput { padding:10px; border:1px solid #d3d3d3; background:#f7f7f7; }
pre.codeoutput { padding:10px 11px; margin:0px 0px 20px; color:#4c4c4c; }
pre.error { color:red; }

@media print { pre.codeinput, pre.codeoutput { word-wrap:break-word; width:100%; } }

span.keyword { color:#0000FF }
span.comment { color:#228B22 }
span.string { color:#A020F0 }
span.untermstring { color:#B20000 }
span.syscmd { color:#B28C00 }
span.typesection { color:#A0522D }

.footer { width:auto; padding:10px 0px; margin:25px 0px 0px; border-top:1px dotted #878787; font-size:0.8em; line-height:140%; font-style:italic; color:#878787; text-align:left; float:none; }
.footer p { margin:0px; }
.footer a { color:#878787; }
.footer a:hover { color:#878787; text-decoration:underline; }
.footer a:visited { color:#878787; }

table th { padding:7px 5px; text-align:left; vertical-align:middle; border: 1px solid #d6d4d4; font-weight:bold; }
table td { padding:7px 5px; text-align:left; vertical-align:top; border:1px solid #d6d4d4; }





  </style></head><body><div class="content"><h2>Contents</h2><div><ul><li><a href="#2">Description</a></li><li><a href="#3">Read image data to matrix: Can be modified</a></li><li><a href="#4">Determine threshold of probable data</a></li><li><a href="#5">Calculate possible centroid regions</a></li><li><a href="#6">Refine centroid regions, modify mask, and calculate centroids</a></li><li><a href="#7">Calculate centroid statistics (separation and rotation)</a></li><li><a href="#8">Find missing data</a></li><li><a href="#9">Find dark/bright "center" of data</a></li><li><a href="#10">Create screen locations based on configuration data (?)</a></li><li><a href="#11">Correlation of beamlet and screen data</a></li><li><a href="#12">Consolidate beamlet data with intensity for each point in beamlet</a></li><li><a href="#13">Update image mask and apply</a></li><li><a href="#14">Rotate 'corr_beamlet' data</a></li><li><a href="#15">Rotate 'beamlet' data</a></li><li><a href="#16">Rotate image</a></li><li><a href="#17">Resize and write image</a></li><li><a href="#18">Store data</a></li><li><a href="#19">Display results</a></li></ul></div><pre class="codeinput"><span class="keyword">function</span> [n_im,cntr,beamlet,r_beamlet,corr_beamlet,r_corr_beamlet] = new_pepper_pot(im_str)
</pre><h2 id="2">Description</h2><p>Used for finding beam data within an image taken from a pepper pot setup and preparing it to be processed to determin beam emittance and twiss parameters.</p><pre class="codeinput"><span class="comment">% Input:</span>
<span class="comment">% im_str - In this form the input is the name of an image file from</span>
<span class="comment">% a pepper pot type system.</span>

<span class="comment">% Outputs:</span>
<span class="comment">% n_im - Fully processed image with noise removed and data rotated to align</span>
<span class="comment">% with the horizontal and vertical axis</span>

<span class="comment">% cntr - Center of the mask used in the pepper pot screen.  Identified as</span>
<span class="comment">% either a dark region or a bright spot, depending on the setup.</span>

<span class="comment">% beamlet - Location and intensity data from the non-rotated image (raw</span>
<span class="comment">% data)</span>

<span class="comment">% r_beamlet - Rotated location and intensity data based on 'beamlet'</span>

<span class="comment">% corr_beamlet - Location information and corresponding screen locations</span>
<span class="comment">% based on the non-rotated image (raw data)</span>

<span class="comment">% r_corr_beamlet - Rotated location information and corresponding screen</span>
<span class="comment">% locations based on corr_beamlet.</span>

<span class="comment">% Created by: Alexander Grabenhofer</span>
<span class="comment">% Created on: 1/30/2020</span>
<span class="comment">% Last update: 6/25/2020</span>
</pre><h2 id="3">Read image data to matrix: Can be modified</h2><p>im_str = input('Input image for processing: ','s');</p><pre class="codeinput">tic;<span class="comment">% for timing purposes only</span>

im = imread(im_str);
im = double(im)./255;

<span class="comment">% check for intensity dependancy (possible RGB colorspace or YUY, or</span>
<span class="comment">% grayscale image.  If we can connect directly to the camera, or know the</span>
<span class="comment">% camera's format, we can modify this to be much simpler.</span>

layers = size(im,3);

<span class="keyword">if</span> layers == 3
    i_12 = abs(im(:,:,1) - im(:,:,2));
    i_23 = abs(im(:,:,2) - im(:,:,3));
    i_13 = abs(im(:,:,1) - im(:,:,3));
    s_12 = sum(sum(i_12));
    s_23 = sum(sum(i_23));
    s_13 = sum(sum(i_13));
    s_tot = s_12 + s_23 + s_13;
    av_i = s_tot / (size(im,1) * size(im,2));
    <span class="keyword">if</span>  av_i == 0 <span class="comment">% all layers are the same</span>
        im = im(:,:,1);
    <span class="keyword">elseif</span> av_i &gt; 0 &amp;&amp; av_i &lt; 0.01 <span class="comment">% all layers are close to the same, majority are identitcal</span>
        im = (im(:,:,1) + im(:,:,2) + im(:,:,3)) ./ 3;
    <span class="keyword">elseif</span> av_i &gt; 0.01 &amp;&amp; av_i &lt;= 0.74 <span class="comment">% rgb colorspace</span>
        im = 0.299 .* im(:,:,1) + 0.587 .* im(:,:,2) + 0.114 .* im(:,:,3);
    <span class="keyword">elseif</span> av_i &gt; 0.74 <span class="comment">% hsv colorspace</span>
        im = im(:,:,1);
    <span class="keyword">end</span>
<span class="keyword">end</span>
</pre><h2 id="4">Determine threshold of probable data</h2><pre class="codeinput">mx = max(max(im));
sd = mean(std(im));
av = mean(mean(im));

<span class="keyword">if</span> av + sd &gt; .01
<span class="comment">%     thresh = mx - 3*(av + sd)</span>
    thresh = av + sd;
<span class="keyword">else</span>
    thresh = .1;
<span class="keyword">end</span>

mask_im = zeros(size(im,1),size(im,2));

<span class="comment">% figure;imagesc(im);colormap(gray);% for showing process</span>
</pre><h2 id="5">Calculate possible centroid regions</h2><pre class="codeinput">summed_row = sum(im,2);
size_r = size(summed_row,1);

summed_col = sum(im,1);
size_c = size(summed_col,2);

m_r = mean(summed_row);
s_r = std(summed_row);

thresh_r = m_r + s_r;

m_c = mean(summed_col);
s_c = std(summed_col);

thresh_c = m_c + s_c;

<span class="comment">% figure;plot(summed_row,'b');hold on;plot(summed_col,'r');axis tight;grid on; %for showing process</span>

<span class="comment">% find the min amd max columns based around the maximum data and threshold</span>
<span class="comment">% value</span>

c_c = 1;
<span class="keyword">for</span> n = 1:1:size(summed_col,2)
    <span class="keyword">if</span> summed_col(n) &lt; thresh_c
        <span class="keyword">continue</span>;
    <span class="keyword">else</span>
        pos_c(c_c,1) = n;
        pos_c(c_c,2) = summed_col(n);
        c_c = c_c + 1;
    <span class="keyword">end</span>
<span class="keyword">end</span>

max_pos = find(pos_c(:,2) == max(pos_c(:,2)));<span class="comment">% replace</span>

sep = diff(pos_c(:,1));<span class="comment">% replace</span>

<span class="comment">% figure;plot(pos_c(:,1),'r');axis tight;hold on;% for showing process</span>
<span class="comment">% plot(sep,'m');axis tight;% for showing process</span>

<span class="keyword">if</span> max(sep) &gt; size_c/10
    sep_thresh_c = mean(sep) + std(sep);
<span class="keyword">else</span>
    sep_thresh_c = size_c/10;
<span class="keyword">end</span>

<span class="keyword">for</span> n = max_pos:-1:1
    <span class="keyword">if</span> n-1 &lt; 1
        <span class="keyword">break</span>
    <span class="keyword">else</span>
        <span class="keyword">if</span> pos_c(n,1) - pos_c(n-1,1) &lt; sep_thresh_c
            <span class="keyword">continue</span>;
        <span class="keyword">else</span>
            <span class="keyword">break</span>;
        <span class="keyword">end</span>
    <span class="keyword">end</span>
<span class="keyword">end</span>

min_c_loc = n;
<span class="comment">% min_c = pos_c(n,1);</span>

<span class="keyword">for</span> n = max_pos:1:size(pos_c,1)
    <span class="keyword">if</span> n+1 &gt; size(pos_c,1)
        <span class="keyword">break</span>
    <span class="keyword">else</span>
        <span class="keyword">if</span> pos_c(n+1,1) - pos_c(n,1) &lt; sep_thresh_c
            <span class="keyword">continue</span>;
        <span class="keyword">else</span>
            <span class="keyword">break</span>;
        <span class="keyword">end</span>
    <span class="keyword">end</span>
<span class="keyword">end</span>

max_c_loc = n;
<span class="comment">% max_c = pos_c(n,1);</span>

<span class="comment">% find the min and max rows based around the maximum data and threshold</span>
<span class="comment">% value</span>

c_r = 1;
<span class="keyword">for</span> n = 1:1:size(summed_row,1)
    <span class="keyword">if</span> summed_row(n) &lt; thresh_r
        <span class="keyword">continue</span>;
    <span class="keyword">else</span>
        pos_r(c_r,1) = n;
        pos_r(c_r,2) = summed_row(n);
        c_r = c_r + 1;
    <span class="keyword">end</span>
<span class="keyword">end</span>

max_pos = find(pos_r(:,2) == max(pos_r(:,2)));<span class="comment">% replace</span>

sep = diff(pos_r(:,1));<span class="comment">% replace</span>

<span class="comment">% plot(pos_r(:,1),'b');% for showing process</span>
<span class="comment">% plot(sep,'c');grid on;hold off;% for showing process</span>

<span class="keyword">if</span> max(sep) &gt; size_r/10
    sep_thresh_r = mean(sep) + std(sep);
<span class="keyword">else</span>
    sep_thresh_r = size_r/10;
<span class="keyword">end</span>

<span class="keyword">for</span> n = max_pos:-1:1
    <span class="keyword">if</span> n-1 &lt; 1
        <span class="keyword">break</span>;
    <span class="keyword">else</span>
        <span class="keyword">if</span> pos_r(n,1) - pos_r(n-1,1) &lt; sep_thresh_r
            <span class="keyword">continue</span>;
        <span class="keyword">else</span>
            <span class="keyword">break</span>;
        <span class="keyword">end</span>
    <span class="keyword">end</span>
<span class="keyword">end</span>

min_r_loc = n;
<span class="comment">% min_r = pos_r(n,1);</span>

<span class="keyword">for</span> n = max_pos:1:size(pos_r,1)
    <span class="keyword">if</span> n+1 &gt; size(pos_r,1)
        <span class="keyword">break</span>;
    <span class="keyword">else</span>
        <span class="keyword">if</span> pos_r(n+1,1) - pos_r(n,1) &lt; sep_thresh_r
            <span class="keyword">continue</span>;
        <span class="keyword">else</span>
            <span class="keyword">break</span>;
        <span class="keyword">end</span>
    <span class="keyword">end</span>
<span class="keyword">end</span>

max_r_loc = n;
<span class="comment">% max_r = pos_r(n,1);</span>

<span class="comment">% figure;imagesc(im);colormap(gray);% for showing steps only</span>
<span class="comment">% hold on;% for showing steps only</span>
<span class="comment">% for r = 1:1:size(pos_r,1)% for showing steps only</span>
<span class="comment">%     for c = 1:1:size(pos_c,1)% for showing steps only</span>
<span class="comment">%         plot(pos_c(c),pos_r(r),'g+');% for showing steps only</span>
<span class="comment">%     end% for showing steps only</span>
<span class="comment">% end% for showing steps only</span>


<span class="comment">% Group data to point locations of min/max for rows and columns</span>

<span class="comment">% column data</span>
n = 1;
pos_c_dat(n,1) = pos_c(min_c_loc);

l_h = 2;
<span class="keyword">for</span> c_c = min_c_loc:1:max_c_loc-1
	<span class="keyword">if</span> pos_c(c_c+1) - pos_c(c_c) &lt; sep_thresh_c/10
		<span class="keyword">if</span> l_h == 1
			pos_c_dat(n,l_h) = pos_c(c_c);
			l_h = l_h + 1;
		<span class="keyword">else</span>
			<span class="keyword">continue</span>;
		<span class="keyword">end</span>
	<span class="keyword">else</span>
		pos_c_dat(n,l_h) = pos_c(c_c);
		<span class="keyword">if</span> l_h == 2
			l_h = 1;
			n = n+1;
		<span class="keyword">else</span>
			l_h = l_h + 1;
		<span class="keyword">end</span>
	<span class="keyword">end</span>
<span class="keyword">end</span>

pos_c_dat(n,2) = pos_c(max_c_loc);


<span class="comment">% row data</span>

n = 1;
pos_r_dat(n,1) = pos_r(min_r_loc);

l_h = 2;
<span class="keyword">for</span> c_r = min_r_loc:1:max_r_loc-1
	<span class="keyword">if</span> pos_r(c_r+1) - pos_r(c_r) &lt; sep_thresh_r/10
		<span class="keyword">if</span> l_h == 1
			pos_r_dat(n,l_h) = pos_r(c_r);
			l_h = l_h + 1;
		<span class="keyword">else</span>
			<span class="keyword">continue</span>;
		<span class="keyword">end</span>
	<span class="keyword">else</span>
		pos_r_dat(n,l_h) = pos_r(c_r);
		<span class="keyword">if</span> l_h == 2
			l_h = 1;
			n = n+1;
		<span class="keyword">else</span>
			l_h = l_h + 1;
		<span class="keyword">end</span>
	<span class="keyword">end</span>
<span class="keyword">end</span>

pos_r_dat(n,2) = pos_r(max_r_loc);


<span class="comment">% figure;imagesc(im);colormap(gray);% for showing steps only</span>
<span class="comment">% hold on;% for showing steps only</span>
<span class="comment">% for r = 1:1:size(pos_r_dat,1)% for showing steps only</span>
<span class="comment">%     for c = 1:1:size(pos_c_dat,1)% for showing steps only</span>
<span class="comment">%         plot(pos_c_dat(c),pos_r_dat(r),'g+');% for showing steps only</span>
<span class="comment">%     end% for showing steps only</span>
<span class="comment">% end% for showing steps only</span>
</pre><h2 id="6">Refine centroid regions, modify mask, and calculate centroids</h2><pre class="codeinput"><span class="comment">% pts = zeros(size(pos_r_dat,1)*size(pos_c_dat,1),2);</span>

n = 1;

<span class="keyword">for</span> c_r = 1:1:size(pos_r_dat,1)
    <span class="keyword">for</span> c_c = 1:1:size(pos_c_dat,1)
        min_r = pos_r_dat(c_r,1);
        max_r = pos_r_dat(c_r,2);
        min_c = pos_c_dat(c_c,1);
        max_c = pos_c_dat(c_c,2);

        <span class="keyword">if</span> min_r &lt; 1 || max_r &gt; size(im,1) || min_c &lt; 1 || max_c &gt; size(im,2)
            <span class="keyword">continue</span>;
        <span class="keyword">end</span>

        chk_im = im(min_r:max_r,min_c:max_c);
        <span class="keyword">if</span> max(max(chk_im)) &lt; (1 - 3 * thresh)
            <span class="keyword">continue</span>;
        <span class="keyword">else</span>
            <span class="comment">% refine centroid max and min</span>
            [chk_r,chk_c] = find(im(min_r:max_r,min_c:max_c) == max(max(chk_im)));<span class="comment">% modify</span>
            chk_r = chk_r(1) + min_r-1;
            chk_c = chk_c(1) + min_c-1;
            cr = chk_r;
            cc = chk_c;

<span class="comment">%                     minimum row calculation</span>
            <span class="keyword">while</span> im(cr,cc) &gt;  thresh
                cr = cr - 1;
                <span class="keyword">if</span> cr == 0
                    <span class="keyword">break</span>;
                <span class="keyword">end</span>
                <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                    cc = cc - 1;
                    <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                        cc = cc + 2;
                    <span class="keyword">end</span>
                <span class="keyword">end</span>
            <span class="keyword">end</span>
            min_r = cr+1;

            cr = chk_r;
            cc = chk_c;
<span class="comment">%                     maximum row calculation</span>
            <span class="keyword">while</span> im(cr,cc) &gt; thresh <span class="comment">% .1</span>
                cr = cr + 1;
                <span class="keyword">if</span> cr &gt; size(im,1)
                    <span class="keyword">break</span>;
                <span class="keyword">end</span>
                <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                    cc = cc - 1;
                    <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                        cc = cc + 2;
                    <span class="keyword">end</span>
                <span class="keyword">end</span>
            <span class="keyword">end</span>
            max_r = cr-1;

            cr = chk_r;
            cc = chk_c;
<span class="comment">%                     mimimum column calculation</span>
            <span class="keyword">while</span> im(cr,cc) &gt; thresh <span class="comment">% .1</span>
                cc = cc - 1;
                <span class="keyword">if</span> cc == 0
                    <span class="keyword">break</span>;
                <span class="keyword">end</span>
                <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                    cr = cr - 1;
                    <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                        cr = cr + 2;
                    <span class="keyword">end</span>
                <span class="keyword">end</span>
            <span class="keyword">end</span>
            min_c = cc+1;

            cr = chk_r;
            cc = chk_c;
<span class="comment">%                     maximum column calculation</span>
            <span class="keyword">while</span> im(cr,cc) &gt; thresh <span class="comment">% .1</span>
                cc = cc + 1;
                <span class="keyword">if</span> cc &gt; size(im,2)
                    <span class="keyword">break</span>;
                <span class="keyword">end</span>
                <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                    cr = cr - 1;
                    <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                        cr = cr + 2;
                    <span class="keyword">end</span>
                <span class="keyword">end</span>
            <span class="keyword">end</span>
            max_c = cc-1;

            <span class="comment">% update mask data</span>
            mask_part = ones(max_r-min_r+1,max_c-min_c+1);
            mask_im(min_r:max_r,min_c:max_c) = mask_part;

            <span class="comment">% calculate centriod</span>
            <span class="comment">% calculate total centroind intensity</span>
            sum_int = 0;
            <span class="keyword">for</span> r = min_r:1:max_r
                <span class="keyword">for</span> c = min_c:1:max_c
                    sum_int = sum_int + im(r,c);
                <span class="keyword">end</span>
            <span class="keyword">end</span>

            <span class="keyword">if</span> sum_int == 0
                <span class="keyword">continue</span>;
            <span class="keyword">end</span>

            <span class="comment">% calculate row centroid</span>
            cent_r = 0;
            <span class="keyword">for</span> r = min_r:1:max_r
                <span class="keyword">for</span> c = min_c:1:max_c
                    cent_r = cent_r + (r * im(r,c));
                <span class="keyword">end</span>
            <span class="keyword">end</span>
            cent_r = cent_r / sum_int;

            <span class="comment">% calculate column centroid</span>
            cent_c = 0;
            <span class="keyword">for</span> c = min_c:1:max_c
                <span class="keyword">for</span> r = min_r:1:max_r
                    cent_c = cent_c + (c * im(r,c));
                <span class="keyword">end</span>
            <span class="keyword">end</span>
            cent_c = cent_c / sum_int;

            pts(n,1) = cent_r;
            pts(n,2) = cent_c;
            pts(n,3) = min_r;
            pts(n,4) = max_r;
            pts(n,5) = min_c;
            pts(n,6) = max_c;
            pts(n,7) = im(round(cent_r),round(cent_c));

            n = n + 1;
        <span class="keyword">end</span>
    <span class="keyword">end</span>
<span class="keyword">end</span>

centroids_found = toc <span class="comment">% timing only</span>

figure;imagesc(im);colormap(gray);<span class="comment">% for showing steps only</span>
hold<span class="comment">% for showing steps only</span>
<span class="keyword">for</span> n = 1:1:size(pts,1)<span class="comment">% for showing steps only</span>
    plot(pts(n,2),pts(n,1),<span class="string">'r+'</span>);<span class="comment">% for showing steps only</span>
    plot(pts(n,5),pts(n,3),<span class="string">'b+'</span>);<span class="comment">% for showing steps only</span>
    plot(pts(n,5),pts(n,4),<span class="string">'b+'</span>);<span class="comment">% for showing steps only</span>
    plot(pts(n,6),pts(n,3),<span class="string">'b+'</span>);<span class="comment">% for showing steps only</span>
    plot(pts(n,6),pts(n,4),<span class="string">'b+'</span>);<span class="comment">% for showing steps only</span>
<span class="keyword">end</span><span class="comment">% for showing steps only</span>

<span class="comment">% figure;imagesc(mask_im);colormap(gray);% for showing steps only</span>

<span class="comment">% figure;imagesc(pro_im);colormap(gray);% for showing steps only</span>
</pre><h2 id="7">Calculate centroid statistics (separation and rotation)</h2><pre class="codeinput"><span class="comment">% calculate distances and angles between points</span>

p = 1;
<span class="keyword">for</span> n1 = 1:1:size(pts,1)
    <span class="keyword">for</span> n2 = 1:1:size(pts,1)
        <span class="keyword">if</span> n1 == n2
            <span class="keyword">continue</span>;
        <span class="keyword">else</span>
            dx = pts(n1,2)-pts(n2,2);
            dy = pts(n1,1)-pts(n2,1);
            d(n1,p) = sqrt(dx^2 + dy^2);
            o(n1,p) = atand(dy/dx);
            p = p + 1;
        <span class="keyword">end</span>
    <span class="keyword">end</span>
    p = 1;
<span class="keyword">end</span>


<span class="comment">% find minimum distances and angles</span>

<span class="keyword">for</span> n = 1:1:size(d,1)
    loc = find(d(n,:) == min(d(n,:)));<span class="comment">% this needs to be changed</span>
    <span class="keyword">if</span> isempty(loc) == 1
        <span class="keyword">continue</span>;
    <span class="keyword">end</span>
    min_d_o(n,1) = d(n,loc(1));
    min_d_o(n,2) = o(n,loc(1));
<span class="keyword">end</span>


<span class="comment">% clean up data</span>
<span class="comment">% remove extra long distances</span>

av_d = mean(min_d_o(:,1));
pt = 1;
<span class="keyword">for</span> n = 1:1:size(min_d_o,1)
    <span class="keyword">if</span> min_d_o(n,1) &gt; av_d
        <span class="keyword">continue</span>;
    <span class="keyword">else</span>
        d_o(pt,1) = min_d_o(n,1);
        d_o(pt,2) = min_d_o(n,2);
        pt = pt+1;
    <span class="keyword">end</span>
<span class="keyword">end</span>

<span class="comment">% remove near 90 degree rotations</span>


<span class="keyword">for</span> n = 1:1:size(d_o,1)
    <span class="keyword">if</span> d_o(n,2) &gt; 45
        d_o(n,2) = 90 - d_o(n,2);
    <span class="keyword">elseif</span> d_o(n,2) &lt; -45
        d_o(n,2) = -90 - d_o(n,2);
    <span class="keyword">end</span>
<span class="keyword">end</span>


<span class="comment">% remove 0 degree rotations</span>

pt = 1;
<span class="keyword">for</span> n = 1:1:size(d_o,1)
    <span class="keyword">if</span> d_o(n,2) == 0
        <span class="keyword">continue</span>;
    <span class="keyword">else</span>
        dat(pt,1) = d_o(n,1);
        dat(pt,2) = d_o(n,2);
        pt = pt + 1;
    <span class="keyword">end</span>
<span class="keyword">end</span>


<span class="comment">% calculate rotation angle</span>

min_d_loc = find(dat(:,1) == min(dat(:,1)));

deg_dir = sign(dat(min_d_loc(1),2));

deg = deg_dir * mean(abs(dat(:,2)))

<span class="keyword">if</span> isequaln(deg,NaN) == 1
    deg = 0;
<span class="keyword">end</span>
</pre><h2 id="8">Find missing data</h2><pre class="codeinput"><span class="comment">% create prediction grid</span>

r_1 = pts(1,1);
c_1 = pts(1,2);

dist = mean(dat(:,1));

sep_h = abs(dist * cosd(deg));
sep_v = abs(dist * sind(deg));

num_step_l = floor(c_1/sep_h);
num_step_r = floor((size(im,2)-c_1)/sep_h);
step_h = num_step_l + num_step_r;

num_step_u = floor(r_1/sep_h);
num_step_d = floor((size(im,1)-r_1)/sep_h);
step_v = num_step_u + num_step_d;

slp = -sign(deg);

<span class="keyword">if</span> slp == 1
    r_0 = (r_1 - (num_step_l * sep_v)) - (num_step_u * sep_h);
    c_0 = (c_1 - (num_step_l * sep_h)) - (num_step_u * sep_v);
<span class="keyword">elseif</span> slp == -1
    r_0 = (r_1 + (num_step_l * sep_v)) - (num_step_u * sep_h);
    c_0 = (c_1 - (num_step_l * sep_h)) - (num_step_u * sep_v);
<span class="keyword">end</span>

n = 1;

r_a = r_0;
c_a = c_0;

step_r = 0;
<span class="keyword">while</span> r_a &lt;= size(im,1)
    <span class="keyword">for</span> step_c = 0:1:step_h
        r = r_a + (slp * step_c * sep_v);
        c = c_a + (step_c * sep_h);
        <span class="keyword">if</span> r &lt; 1 || r &gt; size(im,1)
            <span class="keyword">continue</span>;
        <span class="keyword">end</span>
        <span class="keyword">if</span> c &lt; 1 || c &gt; size(im,2)
            <span class="keyword">continue</span>;
        <span class="keyword">end</span>
        chk_grid(n,1) = round(r);
        chk_grid(n,2) = round(c);
        n = n + 1;
    <span class="keyword">end</span>
    step_r = step_r + 1;
    r_a = r_0 + (step_r * sep_h);
    c_a = c_0 + (-slp * step_r * sep_v);
<span class="keyword">end</span>

figure;imagesc(im);colormap(gray); <span class="comment">% for showing steps</span>
hold <span class="string">on</span>; <span class="comment">% for showing steps</span>
plot(chk_grid(:,2),chk_grid(:,1),<span class="string">'g+'</span>); <span class="comment">% for showing steps</span>

<span class="comment">% Use grid values to search for missing data.</span>

row_rad = floor(min(diff(pts(:,[3 4]),1,2))/2);
col_rad = floor(min(diff(pts(:,[5 6]),1,2))/2);

t_r = min(diff(pts(:,[3 4]),1,2));
t_c = min(diff(pts(:,[5 6]),1,2));

tot_pts = t_r * t_c; <span class="comment">% minimum acceptable size of possible data</span>

n = size(pts,1) + 1;

<span class="keyword">for</span> c_pt = 1:1:size(chk_grid,1)
    min_r = chk_grid(c_pt,1)-row_rad;
    max_r = chk_grid(c_pt,1)+row_rad;
    min_c = chk_grid(c_pt,2)-col_rad;
    max_c = chk_grid(c_pt,2)+col_rad;

    next_pt = 0;

    <span class="comment">%determines if a point is already contained in a centroid</span>
    <span class="keyword">for</span> chk = 1:1:size(pts,1)
        <span class="keyword">if</span> (chk_grid(c_pt,1) &lt;= pts(chk,4) &amp;&amp; chk_grid(c_pt,1) &gt;= pts(chk,3)) &amp;&amp; (chk_grid(c_pt,2) &lt;= pts(chk,6) &amp;&amp; chk_grid(c_pt,2) &gt;= pts(chk,5))
            next_pt = 1;
        <span class="keyword">end</span>
    <span class="keyword">end</span>

    <span class="keyword">if</span> min_r &lt; 1 || max_r &gt; size(im,1) || min_c &lt; 1 || max_c &gt; size(im,2) || next_pt == 1
        <span class="keyword">continue</span>;
    <span class="keyword">end</span>

    chk_im = im(min_r:max_r,min_c:max_c);
    <span class="keyword">if</span> max(max(chk_im)) &lt; thresh
        <span class="keyword">continue</span>;
    <span class="keyword">else</span>
        <span class="comment">% refine centroid max and min</span>
        [chk_r,chk_c] = find(im(min_r:max_r,min_c:max_c) == max(max(chk_im)));<span class="comment">% modify</span>
        chk_r = chk_r(1) + min_r-1;
        chk_c = chk_c(1) + min_c-1;
        cr = chk_r;
        cc = chk_c;

<span class="comment">%                     minimum row calculation</span>
        <span class="keyword">while</span> im(cr,cc) &gt; thresh
            cr = cr - 1;
            <span class="keyword">if</span> cr == 0
                <span class="keyword">break</span>;
            <span class="keyword">end</span>
            <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                cc = cc - 1;
                <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                    cc = cc + 2;
                <span class="keyword">end</span>
            <span class="keyword">end</span>
        <span class="keyword">end</span>
        min_r = cr+1;

        cr = chk_r;
        cc = chk_c;
<span class="comment">%                     maximum row calculation</span>
        <span class="keyword">while</span> im(cr,cc) &gt; thresh <span class="comment">% .1</span>
            cr = cr + 1;
            <span class="keyword">if</span> cr &gt; size(im,1)
                <span class="keyword">break</span>;
            <span class="keyword">end</span>
            <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                cc = cc - 1;
                <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                    cc = cc + 2;
                <span class="keyword">end</span>
            <span class="keyword">end</span>
        <span class="keyword">end</span>
        max_r = cr-1;

        cr = chk_r;
        cc = chk_c;
<span class="comment">%                     mimimum column calculation</span>
        <span class="keyword">while</span> im(cr,cc) &gt; thresh <span class="comment">% .1</span>
            cc = cc - 1;
            <span class="keyword">if</span> cc == 0
                <span class="keyword">break</span>;
            <span class="keyword">end</span>
            <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                cr = cr - 1;
                <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                    cr = cr + 2;
                <span class="keyword">end</span>
            <span class="keyword">end</span>
        <span class="keyword">end</span>
        min_c = cc+1;

        cr = chk_r;
        cc = chk_c;
<span class="comment">%                     maximum column calculation</span>
        <span class="keyword">while</span> im(cr,cc) &gt; thresh <span class="comment">% .1</span>
            cc = cc + 1;
            <span class="keyword">if</span> cc &gt; size(im,2)
                <span class="keyword">break</span>;
            <span class="keyword">end</span>
            <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                cr = cr - 1;
                <span class="keyword">if</span> im(cr,cc) &lt;= thresh <span class="comment">% .1</span>
                    cr = cr + 2;
                <span class="keyword">end</span>
            <span class="keyword">end</span>
        <span class="keyword">end</span>
        max_c = cc-1;

        <span class="comment">% calculate centriod</span>
        <span class="comment">% calculate total centroind intensity</span>
        sum_int = 0;
        sum_pts = 0;
        <span class="keyword">for</span> r = min_r:1:max_r
            <span class="keyword">for</span> c = min_c:1:max_c
                sum_int = sum_int + im(r,c);
                sum_pts = sum_pts + 1;
            <span class="keyword">end</span>
        <span class="keyword">end</span>

        <span class="keyword">if</span> sum_int &lt; thresh * sum_pts || sum_pts &lt;= tot_pts <span class="comment">% thresh * sum_pts</span>
            <span class="keyword">continue</span>;
        <span class="keyword">end</span>

        <span class="comment">% calculate row centroid</span>
        cent_r = 0;
        <span class="keyword">for</span> r = min_r:1:max_r
            <span class="keyword">for</span> c = min_c:1:max_c
                cent_r = cent_r + (r * im(r,c));
            <span class="keyword">end</span>
        <span class="keyword">end</span>
        cent_r = cent_r / sum_int;

        <span class="comment">% calculate column centroid</span>
        cent_c = 0;
        <span class="keyword">for</span> c = min_c:1:max_c
            <span class="keyword">for</span> r = min_r:1:max_r
                cent_c = cent_c + (c * im(r,c));
            <span class="keyword">end</span>
        <span class="keyword">end</span>
        cent_c = cent_c / sum_int;

        pts(n,1) = cent_r;
        pts(n,2) = cent_c;
        pts(n,3) = min_r;
        pts(n,4) = max_r;
        pts(n,5) = min_c;
        pts(n,6) = max_c;
        pts(n,7) = im(round(cent_r),round(cent_c));

        n = n + 1;

    <span class="keyword">end</span>
<span class="keyword">end</span>
</pre><h2 id="9">Find dark/bright "center" of data</h2><pre class="codeinput">m_pts = mean(pts(:,[1 2]));

d_pts = zeros(size(pts,1),3);

<span class="keyword">for</span> n = 1:1:size(pts,1) <span class="comment">% distances from every point to "pre-center"</span>
    d_pts(n,1) = pts(n,1);
    d_pts(n,2) = pts(n,2);
    d_pts(n,3) = sqrt((pts(n,1)-m_pts(1))^2 + (pts(n,2)-m_pts(2))^2);
<span class="keyword">end</span>

<span class="keyword">if</span> min(d_pts) &lt; dist/2 <span class="comment">% check if "pre-center" exists within current data set</span>
    [val,loc] = min(d_pts);
    cntr = pts(loc,[1 2]);
<span class="keyword">else</span> <span class="comment">% calculate actual center based on 8 closest points (8 based on geometric configuration of screen)</span>
    c_pts = zeros(8,2);
    sort_d_pts = sortrows(d_pts,3);
    c_pts = sort_d_pts(1:8,[1 2]);
    cntr = mean(c_pts);
<span class="keyword">end</span>

figure;imagesc(im);colormap(gray);<span class="comment">% for showing steps only</span>
hold<span class="comment">% for showing steps only</span>
<span class="keyword">for</span> n = 1:1:size(pts,1)<span class="comment">% for showing steps only</span>
    plot(pts(n,2),pts(n,1),<span class="string">'r+'</span>);<span class="comment">% for showing steps only</span>
    plot(pts(n,5),pts(n,3),<span class="string">'b+'</span>);<span class="comment">% for showing steps only</span>
    plot(pts(n,5),pts(n,4),<span class="string">'b+'</span>);<span class="comment">% for showing steps only</span>
    plot(pts(n,6),pts(n,3),<span class="string">'b+'</span>);<span class="comment">% for showing steps only</span>
    plot(pts(n,6),pts(n,4),<span class="string">'b+'</span>);<span class="comment">% for showing steps only</span>
<span class="keyword">end</span><span class="comment">% for showing steps only</span>
plot(cntr(2),cntr(1),<span class="string">'gx'</span>);


missing_data_corrected = toc <span class="comment">% timing only</span>
</pre><h2 id="10">Create screen locations based on configuration data (?)</h2><pre class="codeinput"><span class="comment">% input number of holes x/y</span>
num_x = 25; <span class="comment">% modify for different methods of input</span>
num_y = 25; <span class="comment">% modify for different methods of input</span>

<span class="comment">% input hole separation based on pixel (?) data</span>
sep_x = 14;
sep_y = 14; <span class="comment">% modify here as well. presumed square arrangement at this point</span>

<span class="comment">% generate locations</span>
r_1 = cntr(1);
c_1 = cntr(2);

sep_h = abs(sep_x * cosd(deg));
sep_v = abs(sep_x * sind(deg));

num_step_l = floor(num_x/2);
num_step_r = floor(num_x/2);
num_step_u = floor(num_y/2);
num_step_d = floor(num_y/2);

slp = -sign(deg);

<span class="keyword">if</span> slp == 1
    r_0 = (r_1 - (num_step_l * sep_v)) - (num_step_u * sep_h);
    c_0 = (c_1 - (num_step_l * sep_h)) - (num_step_u * sep_v);
<span class="keyword">elseif</span> slp == -1
    r_0 = (r_1 + (num_step_l * sep_v)) - (num_step_u * sep_h);
    c_0 = (c_1 - (num_step_l * sep_h)) - (num_step_u * sep_v);
<span class="keyword">end</span>

n = 1;

r_a = r_0;
c_a = c_0;

step_v = num_step_u + num_step_d;
step_h = num_step_l + num_step_r;

<span class="keyword">for</span> step_r = 0:1:step_v+1
    <span class="keyword">for</span> step_c = 0:1:step_h
        r = r_a + (slp * step_c * sep_v);
        c = c_a + (step_c * sep_h);
        <span class="keyword">if</span> r &lt; 1 || r &gt; size(im,1)
            <span class="keyword">continue</span>;
        <span class="keyword">end</span>
        <span class="keyword">if</span> c &lt; 1 || c &gt; size(im,2)
            <span class="keyword">continue</span>;
        <span class="keyword">end</span>
        scrn_grid(n,1) = round(r);
        scrn_grid(n,2) = round(c);
        n = n + 1;
    <span class="keyword">end</span>
    r_a = r_0 + (step_r * sep_h);
    c_a = c_0 + (-slp * step_r * sep_v);
<span class="keyword">end</span>

figure;imagesc(im);colormap(gray);
hold <span class="string">on</span>;
plot(scrn_grid(:,2),scrn_grid(:,1),<span class="string">'g+'</span>);
</pre><h2 id="11">Correlation of beamlet and screen data</h2><pre class="codeinput">r0 = cntr(1);
c0 = cntr(2);
s_r0 = ceil(num_y/2);
s_c0 = ceil(num_x/2);
pt = 1;

<span class="keyword">for</span> n = 1:1:size(pts,1)
     r = pts(n,1);
     c = pts(n,2);

     step_r = round((r-r0) / dist); <span class="comment">%modify for rotation?</span>
     step_c = round((c-c0) / dist); <span class="comment">%modify for rotation?</span>

     s_r1 = s_r0 + step_r;
     s_c1 = s_c0 + step_c;

     <span class="keyword">if</span> s_r1 &lt; 1 || s_c1 &lt; 1
         <span class="keyword">continue</span>;
     <span class="keyword">end</span>

     screen_num = ((s_r1) * num_x) + s_c1;

     s_r = scrn_grid(screen_num,1);
     s_c = scrn_grid(screen_num,2);

     corr_beamlet(pt,1) = n;
     corr_beamlet(pt,2) = r;
     corr_beamlet(pt,3) = c;
     corr_beamlet(pt,4) = pts(n,3);
     corr_beamlet(pt,5) = pts(n,4);
     corr_beamlet(pt,6) = (pts(n,3) + pts(n,4))/2;
     corr_beamlet(pt,7) = pts(n,5);
     corr_beamlet(pt,8) = pts(n,6);
     corr_beamlet(pt,9) = (pts(n,5) + pts(n,6))/2;
     corr_beamlet(pt,10) = s_r;
     corr_beamlet(pt,11) = s_c;
     pt = pt + 1;
<span class="keyword">end</span>

figure;imagesc(im);colormap(gray); <span class="comment">% for testing purposes</span>
hold <span class="string">on</span>; <span class="comment">% for testing purposes</span>
plot(corr_beamlet(:,3),corr_beamlet(:,2),<span class="string">'g+'</span>); <span class="comment">% for testing purposes</span>
plot(corr_beamlet(:,11),corr_beamlet(:,10),<span class="string">'r+'</span>); <span class="comment">% for testing purposes</span>
plot(scrn_grid(:,2),scrn_grid(:,1),<span class="string">'bx'</span>); <span class="comment">% for testing purposes</span>
plot(cntr(2),cntr(1),<span class="string">'c.'</span>); <span class="comment">% for testing purposes</span>
</pre><h2 id="12">Consolidate beamlet data with intensity for each point in beamlet</h2><pre class="codeinput">n = 1;

<span class="keyword">for</span> b_let = 1:1:size(corr_beamlet,1)
    min_r = corr_beamlet(b_let,4);
    max_r = corr_beamlet(b_let,5);
    min_c = corr_beamlet(b_let,7);
    max_c = corr_beamlet(b_let,8);
    <span class="keyword">for</span> r = min_r:1:max_r
        <span class="keyword">for</span> c = min_c:1:max_c
            beamlet(n,1) = b_let;
            beamlet(n,2) = r;
            beamlet(n,3) = c;
            beamlet(n,4) = im(r,c);
            n = n + 1;
        <span class="keyword">end</span>
    <span class="keyword">end</span>
<span class="keyword">end</span>
</pre><h2 id="13">Update image mask and apply</h2><pre class="codeinput"><span class="keyword">for</span> n = 1:1:size(corr_beamlet,1)
    min_r = corr_beamlet(n,4);
    max_r = corr_beamlet(n,5);
    min_c = corr_beamlet(n,7);
    max_c = corr_beamlet(n,8);
    <span class="keyword">for</span> r = min_r:1:max_r
        <span class="keyword">for</span> c = min_c:1:max_c
            mask_im(r,c) = 1;
        <span class="keyword">end</span>
    <span class="keyword">end</span>
<span class="keyword">end</span>

pro_im = im .* mask_im; <span class="comment">% cleaned image before rotating.</span>
</pre><h2 id="14">Rotate 'corr_beamlet' data</h2><pre class="codeinput"><span class="comment">% setup size contstraints for rotated data</span>
sr = size(pro_im,1);
sc = size(pro_im,2);

<span class="comment">% setup matrix for rotating every point in corr_beamlet by calculated degree</span>
c_pts_xy = zeros(size(corr_beamlet)); <span class="comment">% corr_beamlet initial matrix</span>
c_pts_ro = c_pts_xy; <span class="comment">% r/theta initial matrix</span>
n_c_pts_ro = c_pts_xy; <span class="comment">% r/theta rotated matrix</span>
n_c_pts_xy = c_pts_xy; <span class="comment">% x/y rotated matrix</span>

<span class="comment">% center of image defined for rotation - may need to be modified for the</span>
<span class="comment">% center of the screen.</span>
cx = cntr(2); <span class="comment">% sc/2; screen center (old is image center)</span>
cy = cntr(1); <span class="comment">% sr/2; screen center (old is image center)</span>

<span class="comment">% populate initial x/y/intensity matrix for conversion to r/theta/intensity</span>
<span class="comment">% matrix (centered around centre of image)</span>
<span class="keyword">for</span> r = 1:1:size(corr_beamlet,1)
    c_pts_xy(r,1) = corr_beamlet(r,1);<span class="comment">% beamlet # (constant)</span>
    c_pts_xy(r,2) = corr_beamlet(r,3)-cx+1;<span class="comment">% beamlet x centroid</span>
    c_pts_xy(r,3) = corr_beamlet(r,2)-cy+1;<span class="comment">% beamlet y centroid</span>
    c_pts_xy(r,4) = corr_beamlet(r,4)-cy+1;<span class="comment">% beamlet y minimum</span>
    c_pts_xy(r,5) = corr_beamlet(r,5)-cy+1;<span class="comment">% beamlet y maximum</span>
    c_pts_xy(r,6) = corr_beamlet(r,6)-cy+1;<span class="comment">% beamlet y center</span>
    c_pts_xy(r,7) = corr_beamlet(r,7)-cx+1;<span class="comment">% beamlet x minimum</span>
    c_pts_xy(r,8) = corr_beamlet(r,8)-cx+1;<span class="comment">% beamlet x maximum</span>
    c_pts_xy(r,9) = corr_beamlet(r,9)-cx+1;<span class="comment">% beamlet x center</span>
    c_pts_xy(r,10) = corr_beamlet(r,11)-cx+1;<span class="comment">% beamlet screen x center</span>
    c_pts_xy(r,11) = corr_beamlet(r,10)-cy+1;<span class="comment">% beamlet screen y center</span>
<span class="keyword">end</span>

clear <span class="string">n</span>;

<span class="comment">% convert to r/theta matrix</span>
<span class="keyword">for</span> n = 1:1:size(c_pts_xy,1)
    x = c_pts_xy(n,2);
    y = c_pts_xy(n,3);

    x_min = c_pts_xy(n,7);
    y_min = c_pts_xy(n,4);

    x_max = c_pts_xy(n,8);
    y_max = c_pts_xy(n,5);

    x_cent = c_pts_xy(n,9);
    y_cent = c_pts_xy(n,6);

    scrn_x = c_pts_xy(n,10);
    scrn_y = c_pts_xy(n,11);

    r = sqrt((x)^2 + (y)^2);
    theta = abs(atand((y)/(x)));

    r_min = sqrt((x_min)^2 + (y_min)^2);
    theta_min = abs(atand((y_min)/(x_min)));

    r_max = sqrt((x_max)^2 + (y_max)^2);
    theta_max = abs(atand((y_max)/(x_max)));

    r_cent = sqrt((x_cent)^2 + (y_cent)^2);
    theta_cent = abs(atand((y_cent)/(x_cent)));

    r_scrn = sqrt((scrn_x)^2 + (scrn_y)^2);
    theta_scrn = abs(atand((scrn_y)/(scrn_x)));

    <span class="comment">% conditions for rotation depend on initial x/y location relative to</span>
    <span class="comment">% center</span>
    <span class="keyword">if</span> x &lt; 0 &amp;&amp; y &gt; 0
        theta = 180 - theta;
    <span class="keyword">elseif</span> x &gt; 0 &amp;&amp; y &gt; 0
        theta = theta;
    <span class="keyword">elseif</span> x &gt; 0 &amp;&amp; y &lt; 0
        theta = 360 - theta;
    <span class="keyword">elseif</span> x &lt; 0 &amp;&amp; y &lt; 0
        theta = 180 + theta;
    <span class="keyword">end</span>

    <span class="keyword">if</span> x_min &lt; 0 &amp;&amp; y_min &gt; 0
        theta_min = 180 - theta_min;
    <span class="keyword">elseif</span> x_min &gt; 0 &amp;&amp; y_min &gt; 0
        theta_min = theta_min;
    <span class="keyword">elseif</span> x_min &gt; 0 &amp;&amp; y_min &lt; 0
        theta_min = 360 - theta_min;
    <span class="keyword">elseif</span> x_min &lt; 0 &amp;&amp; y_min &lt; 0
        theta_min = 180 + theta_min;
    <span class="keyword">end</span>

    <span class="keyword">if</span> x_max &lt; 0 &amp;&amp; y_max &gt; 0
        theta_max = 180 - theta_max;
    <span class="keyword">elseif</span> x_max &gt; 0 &amp;&amp; y_max &gt; 0
        theta_max = theta_max;
    <span class="keyword">elseif</span> x_max &gt; 0 &amp;&amp; y_max &lt; 0
        theta_max = 360 - theta_max;
    <span class="keyword">elseif</span> x_max &lt; 0 &amp;&amp; y_max &lt; 0
        theta_max = 180 + theta_max;
    <span class="keyword">end</span>

    <span class="keyword">if</span> x_cent &lt; 0 &amp;&amp; y_cent &gt; 0
        theta_cent = 180 - theta_cent;
    <span class="keyword">elseif</span> x_cent &gt; 0 &amp;&amp; y_cent &gt; 0
        theta_cent = theta_cent;
    <span class="keyword">elseif</span> x_cent &gt; 0 &amp;&amp; y_cent &lt; 0
        theta_cent = 360 - theta_cent;
    <span class="keyword">elseif</span> x_cent &lt; 0 &amp;&amp; y_cent &lt; 0
        theta_cent = 180 + theta_cent;
    <span class="keyword">end</span>

    <span class="keyword">if</span> scrn_x &lt; 0 &amp;&amp; scrn_y &gt; 0
        theta_scrn = 180 - theta_scrn;
    <span class="keyword">elseif</span> scrn_x &gt; 0 &amp;&amp; scrn_y &gt; 0
        theta_scrn = theta_scrn;
    <span class="keyword">elseif</span> scrn_x &gt; 0 &amp;&amp; scrn_y &lt; 0
        theta_scrn = 360 - theta_scrn;
    <span class="keyword">elseif</span> scrn_x &lt; 0 &amp;&amp; scrn_y &lt; 0
        theta_scrn = 180 + theta_scrn;
    <span class="keyword">end</span>

    c_pts_ro(n,1) = c_pts_xy(n,1);
    c_pts_ro(n,2) = r;
    c_pts_ro(n,3) = theta;
    c_pts_ro(n,4) = r_min;
    c_pts_ro(n,5) = theta_min;
    c_pts_ro(n,6) = r_max;
    c_pts_ro(n,7) = theta_max;
    c_pts_ro(n,8) = r_cent;
    c_pts_ro(n,9) = theta_cent;
    c_pts_ro(n,10) = r_scrn;
    c_pts_ro(n,11) = theta_scrn;

<span class="keyword">end</span>

<span class="comment">% add rotation to r/theta matrix</span>
n_c_pts_ro = c_pts_ro;
n_c_pts_ro(:,3) = c_pts_ro(:,3) + deg;<span class="comment">% theta</span>
n_c_pts_ro(:,5) = c_pts_ro(:,5) + deg;<span class="comment">% theta min</span>
n_c_pts_ro(:,7) = c_pts_ro(:,7) + deg;<span class="comment">% theta max</span>
n_c_pts_ro(:,9) = c_pts_ro(:,9) + deg;<span class="comment">% theta cent</span>
n_c_pts_ro(:,11) = c_pts_ro(:,11) + deg;<span class="comment">% theta screen</span>

<span class="comment">% convert back to x/y form</span>
<span class="keyword">for</span>  n = 1:1:size(n_c_pts_ro,1)
    r = n_c_pts_ro(n,2);
    theta = n_c_pts_ro(n,3);

    r_min = n_c_pts_ro(n,4);
    theta_min = n_c_pts_ro(n,5);

    r_max = n_c_pts_ro(n,6);
    theta_max = n_c_pts_ro(n,7);

    r_cent = n_c_pts_ro(n,8);
    theta_cent = n_c_pts_ro(n,9);

    r_srcn = n_c_pts_ro(n,10);
    theta_scrn = n_c_pts_ro(n,11);

    x = r * cosd(theta) + cx;
    y = r * sind(theta) + cy;

    x_min = r_min * cosd(theta_min) + cx;
    y_min = r_min * sind(theta_min) + cy;

    x_max = r_max * cosd(theta_max) + cx;
    y_max = r_max * sind(theta_max) + cy;

    x_cent = r_cent * cosd(theta_cent) + cx;
    y_cent = r_cent * sind(theta_cent) + cy;

    scrn_x = r_scrn * cosd(theta_scrn) + cx;
    scrn_y = r_scrn * sind(theta_scrn) + cy;

    n_c_pts_xy(n,1) = n_c_pts_ro(n,1);
    n_c_pts_xy(n,2) = y;
    n_c_pts_xy(n,3) = x;
    n_c_pts_xy(n,4) = y_min;
    n_c_pts_xy(n,5) = y_max;
    n_c_pts_xy(n,6) = y_cent;
    n_c_pts_xy(n,7) = x_min;
    n_c_pts_xy(n,8) = x_max;
    n_c_pts_xy(n,9) = x_cent;
    n_c_pts_xy(n,10) = scrn_y;
    n_c_pts_xy(n,11) = scrn_x;
<span class="keyword">end</span>

r_corr_beamlet(:,1) = n_c_pts_xy(:,1);
r_corr_beamlet(:,2) = n_c_pts_xy(:,2)-1;<span class="comment">% + abs(min(n_c_pts_xy(:,1)));</span>
r_corr_beamlet(:,3) = n_c_pts_xy(:,3)-1;<span class="comment">% + abs(min(n_c_pts_xy(:,2)));</span>
r_corr_beamlet(:,4) = n_c_pts_xy(:,4)-1;<span class="comment">% + abs(min(n_c_pts_xy(:,3)));</span>
r_corr_beamlet(:,5) = n_c_pts_xy(:,5)-1;<span class="comment">% + abs(min(n_c_pts_xy(:,4)));</span>
r_corr_beamlet(:,6) = n_c_pts_xy(:,6)-1;<span class="comment">% + abs(min(n_c_pts_xy(:,5)));</span>
r_corr_beamlet(:,7) = n_c_pts_xy(:,7)-1;<span class="comment">% + abs(min(n_c_pts_xy(:,6)));</span>
r_corr_beamlet(:,8) = n_c_pts_xy(:,8)-1;
r_corr_beamlet(:,9) = n_c_pts_xy(:,9)-1;
r_corr_beamlet(:,10) = n_c_pts_xy(:,10)-1;
r_corr_beamlet(:,11) = n_c_pts_xy(:,11)-1;
</pre><h2 id="15">Rotate 'beamlet' data</h2><pre class="codeinput"><span class="comment">% setup size contstraints for rotated data</span>
sr = size(pro_im,1);
sc = size(pro_im,2);

<span class="comment">% setup matrix for rotating every point in corr_beamlet by calculated degree</span>
c_pts_xy = zeros(size(beamlet)); <span class="comment">% corr_beamlet initial matrix</span>
c_pts_ro = c_pts_xy; <span class="comment">% r/theta initial matrix</span>
n_c_pts_ro = c_pts_xy; <span class="comment">% r/theta rotated matrix</span>
n_c_pts_xy = c_pts_xy; <span class="comment">% x/y rotated matrix</span>

<span class="comment">% center of image defined for rotation - may need to be modified for the</span>
<span class="comment">% center of the screen.</span>
cx = cntr(2); <span class="comment">% sc/2; screen center (old is image center)</span>
cy = cntr(1); <span class="comment">% sr/2; screen center (old is image center)</span>

<span class="comment">% populate initial x/y/intensity matrix for conversion to r/theta/intensity</span>
<span class="comment">% matrix (centered around centre of image)</span>
<span class="keyword">for</span> r = 1:1:size(beamlet,1)
    c_pts_xy(r,1) = beamlet(r,1);<span class="comment">% beamlet # (constant)</span>
    c_pts_xy(r,2) = beamlet(r,3)-cx+1;<span class="comment">% beamlet x location</span>
    c_pts_xy(r,3) = beamlet(r,2)-cy+1;<span class="comment">% beamlet y location</span>
    c_pts_xy(r,4) = beamlet(r,4);<span class="comment">% intensity</span>
<span class="keyword">end</span>

clear <span class="string">n</span>;

<span class="comment">% convert to r/theta/intensity matrix</span>
<span class="keyword">for</span> n = 1:1:size(c_pts_xy,1)
    x = c_pts_xy(n,2);
    y = c_pts_xy(n,3);

    r = sqrt((x)^2 + (y)^2);
    theta = abs(atand((y)/(x)));

    <span class="comment">% conditions for rotation depend on initial x/y location relative to</span>
    <span class="comment">% center</span>
    <span class="keyword">if</span> x &lt; 0 &amp;&amp; y &gt; 0
        theta = 180 - theta;
    <span class="keyword">elseif</span> x &gt; 0 &amp;&amp; y &gt; 0
        theta = theta;
    <span class="keyword">elseif</span> x &gt; 0 &amp;&amp; y &lt; 0
        theta = 360 - theta;
    <span class="keyword">elseif</span> x &lt; 0 &amp;&amp; y &lt; 0
        theta = 180 + theta;
    <span class="keyword">end</span>

    c_pts_ro(n,1) = c_pts_xy(n,1);
    c_pts_ro(n,2) = r;
    c_pts_ro(n,3) = theta;
    c_pts_ro(n,4) = c_pts_xy(n,4);

<span class="keyword">end</span>

<span class="comment">% add rotation to r/theta matrix</span>
n_c_pts_ro = c_pts_ro;
n_c_pts_ro(:,3) = c_pts_ro(:,3) + deg;<span class="comment">% theta</span>

<span class="comment">% convert back to x/y form</span>
<span class="keyword">for</span>  n = 1:1:size(n_c_pts_ro,1)
    r = n_c_pts_ro(n,2);
    theta = n_c_pts_ro(n,3);

    x = r * cosd(theta) + cx;
    y = r * sind(theta) + cy;

    n_c_pts_xy(n,1) = n_c_pts_ro(n,1);
    n_c_pts_xy(n,2) = y;
    n_c_pts_xy(n,3) = x;
    n_c_pts_xy(n,4) = n_c_pts_ro(n,4);
<span class="keyword">end</span>

r_beamlet(:,1) = n_c_pts_xy(:,1);
r_beamlet(:,2) = n_c_pts_xy(:,2)-1;<span class="comment">% + abs(min(n_c_pts_xy(:,1)));</span>
r_beamlet(:,3) = n_c_pts_xy(:,3)-1;<span class="comment">% + abs(min(n_c_pts_xy(:,2)));</span>
r_beamlet(:,4) = n_c_pts_xy(:,4);


beamlet_data_rotated = toc <span class="comment">% for timing purposes</span>
</pre><h2 id="16">Rotate image</h2><pre class="codeinput"><span class="comment">% setup size contstraints for rotated image</span>
sr = size(pro_im,1);
sc = size(pro_im,2);

<span class="comment">% setup matrix for rotating every point in image by calculated degree</span>
c_im_xy = zeros(sr*sc,3); <span class="comment">% x/y/intensity initial matrix</span>
c_im_ro = c_im_xy; <span class="comment">% r/theta/intensity initial matrix</span>
n_c_im_ro = c_im_xy; <span class="comment">% r/theta/intensity rotated matrix</span>
n_c_im_xy = c_im_xy; <span class="comment">% x/y/intensity rotated matrix</span>

<span class="comment">% center of image definced for rotation - may need to be modified for the</span>
<span class="comment">% center of the screen.</span>
cx = sc/2;
cy = sr/2;

c_n = 1;

n = 1;

<span class="comment">% populate initial x/y/intensity matrix for conversion to r/theta/intensity</span>
<span class="comment">% matrix</span>
<span class="keyword">for</span> r = 1:1:sr
    <span class="keyword">for</span> c = 1:1:sc
        c_im_xy(n,1) = c-cx+1;
        c_im_xy(n,2) = r-cy+1;
        c_im_xy(n,3) = pro_im(r,c);
        n = n+1;
    <span class="keyword">end</span>
<span class="keyword">end</span>

clear <span class="string">n</span>;

<span class="comment">% convert to r/theta/intensity matrix</span>
<span class="keyword">for</span> n = 1:1:size(c_im_xy,1)
    x = c_im_xy(n,1);
    y = c_im_xy(n,2);

    r = sqrt((x)^2 + (y)^2);
    theta = abs(atand((y)/(x)));
    <span class="comment">% conditions for rotation depend on initial x/y location relative to</span>
    <span class="comment">% center</span>
    <span class="keyword">if</span> x &lt; 0 &amp;&amp; y &gt; 0
        theta = 180 - theta;
    <span class="keyword">elseif</span> x &gt; 0 &amp;&amp; y &gt; 0
        theta = theta;
    <span class="keyword">elseif</span> x &gt; 0 &amp;&amp; y &lt; 0
        theta = 360 - theta;
    <span class="keyword">elseif</span> x &lt; 0 &amp;&amp; y &lt; 0
        theta = 180 + theta;
    <span class="keyword">end</span>
    c_im_ro(n,1) = r;
    c_im_ro(n,2) = theta;
    c_im_ro(n,3) = c_im_xy(n,3);
<span class="keyword">end</span>

<span class="comment">% add rotation to r/theta/intensity matrix</span>
n_c_im_ro = c_im_ro;
n_c_im_ro(:,2) = c_im_ro(:,2) + deg;

<span class="comment">% convert back to x/y/intensity form</span>
<span class="keyword">for</span>  n = 1:1:size(n_c_im_ro,1)
    r = n_c_im_ro(n,1);
    theta = n_c_im_ro(n,2);

    x = r * cosd(theta) + cx;
    y = r * sind(theta) + cy;

    n_c_im_xy(n,1) = x;
    n_c_im_xy(n,2) = y;
    n_c_im_xy(n,3) = n_c_im_ro(n,3);
<span class="keyword">end</span>

n_c_im_xy(:,1) = n_c_im_xy(:,1) + abs(min(n_c_im_xy(:,1)));
n_c_im_xy(:,2) = n_c_im_xy(:,2) + abs(min(n_c_im_xy(:,2)));

<span class="comment">% convert to image from location (since image is only whole numbers, some</span>
<span class="comment">% data may be close, overlap, or be missing</span>
<span class="keyword">for</span> n = 1:1:size(n_c_im_xy,1)
    x = round(n_c_im_xy(n,1));
    <span class="keyword">if</span> isequaln(x,NaN)
        x = cx;
    <span class="keyword">elseif</span> x &lt;= 0
        x = 1;
    <span class="keyword">end</span>
    y = round(n_c_im_xy(n,2));
    <span class="keyword">if</span> isequaln(y,NaN)
        y = cy;
    <span class="keyword">elseif</span> y &lt;= 0
        y = 1;
    <span class="keyword">end</span>
    v = n_c_im_xy(n,3);
    n_im(y,x) = v;
<span class="keyword">end</span>

<span class="comment">% figure;imagesc(n_im);colormap(gray);% for showing process</span>

<span class="comment">% black pixel removeal / fix missing data</span>

<span class="keyword">for</span> r = 2:1:size(n_im,1)-1
    <span class="keyword">for</span> c = 2:1:size(n_im,2)-1
        <span class="keyword">if</span> n_im(r,c) == 0 || isequaln(n_im(r,c),NaN) == 1
            av_i = 0;
            n = 0;
            <span class="keyword">for</span> nr = -1:1:1
                <span class="keyword">for</span> nc = -1:1:1
                    <span class="keyword">if</span> c+nc == c &amp;&amp; r+nr == r
                        <span class="keyword">continue</span>;
                    <span class="keyword">else</span>
                        v = n_im(r+nr,c+nc);
                        <span class="keyword">if</span> v == 0 || isequaln(v,NaN) == 1
                            <span class="keyword">continue</span>
                        <span class="keyword">else</span>
                            av_i = av_i + v;
                            n = n + 1;
                        <span class="keyword">end</span>
                    <span class="keyword">end</span>
                <span class="keyword">end</span>
            <span class="keyword">end</span>
            <span class="keyword">if</span> n &gt; 4
                n_im(r,c) = av_i / n;
            <span class="keyword">else</span>
                n_im(r,c) = 0;
            <span class="keyword">end</span>
        <span class="keyword">end</span>
    <span class="keyword">end</span>
<span class="keyword">end</span>
</pre><h2 id="17">Resize and write image</h2><pre class="codeinput">r_dim = size(n_im,1);
c_dim = size(n_im,2);

sized_im = zeros(size_r,size_c);

r_start = round((r_dim - size_r)/2);
c_start = round((c_dim - size_c)/2);

sized_im = n_im(r_start:size_r+r_start-1,c_start:size_c+c_start-1);
n_im = sized_im;


image_rotated = toc <span class="comment">% for timing purposes</span>
</pre><h2 id="18">Store data</h2><pre class="codeinput">imwrite(pro_im,[<span class="string">'cleaned_'</span>,im_str]);
imwrite(n_im,[<span class="string">'processed_'</span>,im_str]);

c_mat_str = {<span class="string">'beamlet #'</span>,<span class="string">'centroid row (y)'</span>,<span class="string">'centroid col (x)'</span>,<span class="string">'min row'</span>,<span class="string">'max row'</span>,<span class="string">'center row'</span>,<span class="string">'min col'</span>,<span class="string">'max col'</span>,<span class="string">'center col'</span>,<span class="string">'screen center row'</span>,<span class="string">'screen center col'</span>};
mat_str = {<span class="string">'beamlet #'</span>,<span class="string">'row (y)'</span>,<span class="string">'col (x)'</span>,<span class="string">'intensity'</span>};

writecell(c_mat_str(1:11),[<span class="string">'non-rotated_correlated_beamlet_data_for_'</span>,im_str(1:end-4),<span class="string">'.xls'</span>],<span class="string">'Sheet'</span>,1,<span class="string">'Range'</span>,<span class="string">'A1'</span>);
writematrix(corr_beamlet,[<span class="string">'non-rotated_correlated_beamlet_data_for_'</span>,im_str(1:end-4),<span class="string">'.xls'</span>],<span class="string">'Sheet'</span>,1,<span class="string">'Range'</span>,<span class="string">'A2'</span>);

writecell(c_mat_str(1:11),[<span class="string">'rotated_correlated_beamlet_data_for_'</span>,im_str(1:end-4),<span class="string">'.xls'</span>],<span class="string">'Sheet'</span>,1,<span class="string">'Range'</span>,<span class="string">'A1'</span>);
writematrix(r_corr_beamlet,[<span class="string">'rotated_correlated_beamlet_data_for_'</span>,im_str(1:end-4),<span class="string">'.xls'</span>],<span class="string">'Sheet'</span>,1,<span class="string">'Range'</span>,<span class="string">'A2'</span>);

writecell(mat_str(1:4),[<span class="string">'non-rotated_beamlets_for_'</span>,im_str(1:end-4),<span class="string">'.xls'</span>],<span class="string">'Sheet'</span>,1,<span class="string">'Range'</span>,<span class="string">'A1'</span>);
writematrix(beamlet,[<span class="string">'non-rotated_beamlets_for_'</span>,im_str(1:end-4),<span class="string">'.xls'</span>],<span class="string">'Sheet'</span>,1,<span class="string">'Range'</span>,<span class="string">'A2'</span>);

writecell(mat_str(1:4),[<span class="string">'rotated_beamlets_for_'</span>,im_str(1:end-4),<span class="string">'.xls'</span>],<span class="string">'Sheet'</span>,1,<span class="string">'Range'</span>,<span class="string">'A1'</span>);
writematrix(r_beamlet,[<span class="string">'rotated_beamlets_for_'</span>,im_str(1:end-4),<span class="string">'.xls'</span>],<span class="string">'Sheet'</span>,1,<span class="string">'Range'</span>,<span class="string">'A2'</span>);
</pre><h2 id="19">Display results</h2><pre class="codeinput">figure;
subplot(1,2,1);imagesc(im);colormap(gray);
subplot(1,2,2);imagesc(n_im);colormap(gray);
<span class="comment">% figure;imagesc(n_im);colormap(gray);% for showing steps only</span>

program_finished = toc <span class="comment">%for timing purposes only</span>
</pre><pre class="codeoutput error">Error using evalin
Unrecognized function or variable 'im'.
</pre><p class="footer"><br><a href="https://www.mathworks.com/products/matlab/">Published with MATLAB&reg; R2020a</a><br></p></div><!--
##### SOURCE BEGIN #####
function [n_im,cntr,beamlet,r_beamlet,corr_beamlet,r_corr_beamlet] = new_pepper_pot(im_str)
%% Description
% Used for finding beam data within an image taken from a pepper pot setup
% and preparing it to be processed to determin beam emittance and twiss
% parameters.

% Input: 
% im_str - In this form the input is the name of an image file from
% a pepper pot type system.

% Outputs:
% n_im - Fully processed image with noise removed and data rotated to align
% with the horizontal and vertical axis

% cntr - Center of the mask used in the pepper pot screen.  Identified as
% either a dark region or a bright spot, depending on the setup.

% beamlet - Location and intensity data from the non-rotated image (raw
% data)

% r_beamlet - Rotated location and intensity data based on 'beamlet'

% corr_beamlet - Location information and corresponding screen locations
% based on the non-rotated image (raw data)

% r_corr_beamlet - Rotated location information and corresponding screen
% locations based on corr_beamlet.

% Created by: Alexander Grabenhofer
% Created on: 1/30/2020
% Last update: 6/25/2020


%% Read image data to matrix: Can be modified
% im_str = input('Input image for processing: ','s');

tic;% for timing purposes only

im = imread(im_str);
im = double(im)./255;

% check for intensity dependancy (possible RGB colorspace or YUY, or
% grayscale image.  If we can connect directly to the camera, or know the
% camera's format, we can modify this to be much simpler.

layers = size(im,3);

if layers == 3
    i_12 = abs(im(:,:,1) - im(:,:,2));
    i_23 = abs(im(:,:,2) - im(:,:,3));
    i_13 = abs(im(:,:,1) - im(:,:,3));
    s_12 = sum(sum(i_12));
    s_23 = sum(sum(i_23));
    s_13 = sum(sum(i_13));
    s_tot = s_12 + s_23 + s_13;
    av_i = s_tot / (size(im,1) * size(im,2));
    if  av_i == 0 % all layers are the same
        im = im(:,:,1);
    elseif av_i > 0 && av_i < 0.01 % all layers are close to the same, majority are identitcal
        im = (im(:,:,1) + im(:,:,2) + im(:,:,3)) ./ 3;
    elseif av_i > 0.01 && av_i <= 0.74 % rgb colorspace
        im = 0.299 .* im(:,:,1) + 0.587 .* im(:,:,2) + 0.114 .* im(:,:,3);
    elseif av_i > 0.74 % hsv colorspace
        im = im(:,:,1);
    end
end


%% Determine threshold of probable data
mx = max(max(im));
sd = mean(std(im));
av = mean(mean(im));

if av + sd > .01
%     thresh = mx - 3*(av + sd)
    thresh = av + sd;
else
    thresh = .1;
end
    
mask_im = zeros(size(im,1),size(im,2));

% figure;imagesc(im);colormap(gray);% for showing process


%% Calculate possible centroid regions

summed_row = sum(im,2);
size_r = size(summed_row,1);

summed_col = sum(im,1);
size_c = size(summed_col,2);

m_r = mean(summed_row);
s_r = std(summed_row);

thresh_r = m_r + s_r;

m_c = mean(summed_col);
s_c = std(summed_col);

thresh_c = m_c + s_c;

% figure;plot(summed_row,'b');hold on;plot(summed_col,'r');axis tight;grid on; %for showing process

% find the min amd max columns based around the maximum data and threshold
% value

c_c = 1;
for n = 1:1:size(summed_col,2)
    if summed_col(n) < thresh_c
        continue;
    else
        pos_c(c_c,1) = n;
        pos_c(c_c,2) = summed_col(n);
        c_c = c_c + 1;
    end
end

max_pos = find(pos_c(:,2) == max(pos_c(:,2)));% replace

sep = diff(pos_c(:,1));% replace

% figure;plot(pos_c(:,1),'r');axis tight;hold on;% for showing process
% plot(sep,'m');axis tight;% for showing process

if max(sep) > size_c/10
    sep_thresh_c = mean(sep) + std(sep);
else
    sep_thresh_c = size_c/10;
end

for n = max_pos:-1:1
    if n-1 < 1
        break
    else
        if pos_c(n,1) - pos_c(n-1,1) < sep_thresh_c
            continue;
        else
            break;
        end
    end
end

min_c_loc = n;
% min_c = pos_c(n,1);

for n = max_pos:1:size(pos_c,1)
    if n+1 > size(pos_c,1)
        break
    else
        if pos_c(n+1,1) - pos_c(n,1) < sep_thresh_c
            continue;
        else
            break;
        end
    end
end

max_c_loc = n;
% max_c = pos_c(n,1);

% find the min and max rows based around the maximum data and threshold
% value

c_r = 1;
for n = 1:1:size(summed_row,1)
    if summed_row(n) < thresh_r
        continue;
    else
        pos_r(c_r,1) = n;
        pos_r(c_r,2) = summed_row(n);
        c_r = c_r + 1;
    end
end

max_pos = find(pos_r(:,2) == max(pos_r(:,2)));% replace

sep = diff(pos_r(:,1));% replace

% plot(pos_r(:,1),'b');% for showing process
% plot(sep,'c');grid on;hold off;% for showing process

if max(sep) > size_r/10
    sep_thresh_r = mean(sep) + std(sep);
else
    sep_thresh_r = size_r/10;
end

for n = max_pos:-1:1
    if n-1 < 1
        break;
    else
        if pos_r(n,1) - pos_r(n-1,1) < sep_thresh_r
            continue;
        else
            break;
        end
    end
end

min_r_loc = n;
% min_r = pos_r(n,1);

for n = max_pos:1:size(pos_r,1)
    if n+1 > size(pos_r,1)
        break;
    else
        if pos_r(n+1,1) - pos_r(n,1) < sep_thresh_r
            continue;
        else
            break;
        end
    end
end

max_r_loc = n;
% max_r = pos_r(n,1);

% figure;imagesc(im);colormap(gray);% for showing steps only
% hold on;% for showing steps only
% for r = 1:1:size(pos_r,1)% for showing steps only
%     for c = 1:1:size(pos_c,1)% for showing steps only
%         plot(pos_c(c),pos_r(r),'g+');% for showing steps only
%     end% for showing steps only
% end% for showing steps only


% Group data to point locations of min/max for rows and columns

% column data
n = 1;
pos_c_dat(n,1) = pos_c(min_c_loc);

l_h = 2;
for c_c = min_c_loc:1:max_c_loc-1
	if pos_c(c_c+1) - pos_c(c_c) < sep_thresh_c/10
		if l_h == 1
			pos_c_dat(n,l_h) = pos_c(c_c);
			l_h = l_h + 1;
		else
			continue;
		end
	else
		pos_c_dat(n,l_h) = pos_c(c_c);
		if l_h == 2
			l_h = 1;
			n = n+1;
		else
			l_h = l_h + 1;
		end
	end
end

pos_c_dat(n,2) = pos_c(max_c_loc);


% row data

n = 1;
pos_r_dat(n,1) = pos_r(min_r_loc);

l_h = 2;
for c_r = min_r_loc:1:max_r_loc-1
	if pos_r(c_r+1) - pos_r(c_r) < sep_thresh_r/10
		if l_h == 1
			pos_r_dat(n,l_h) = pos_r(c_r);
			l_h = l_h + 1;
		else
			continue;
		end
	else
		pos_r_dat(n,l_h) = pos_r(c_r);
		if l_h == 2
			l_h = 1;
			n = n+1;
		else
			l_h = l_h + 1;
		end
	end
end

pos_r_dat(n,2) = pos_r(max_r_loc);


% figure;imagesc(im);colormap(gray);% for showing steps only
% hold on;% for showing steps only
% for r = 1:1:size(pos_r_dat,1)% for showing steps only
%     for c = 1:1:size(pos_c_dat,1)% for showing steps only
%         plot(pos_c_dat(c),pos_r_dat(r),'g+');% for showing steps only
%     end% for showing steps only
% end% for showing steps only

%% Refine centroid regions, modify mask, and calculate centroids

% pts = zeros(size(pos_r_dat,1)*size(pos_c_dat,1),2);

n = 1;

for c_r = 1:1:size(pos_r_dat,1)
    for c_c = 1:1:size(pos_c_dat,1)
        min_r = pos_r_dat(c_r,1);
        max_r = pos_r_dat(c_r,2);
        min_c = pos_c_dat(c_c,1);
        max_c = pos_c_dat(c_c,2);
        
        if min_r < 1 || max_r > size(im,1) || min_c < 1 || max_c > size(im,2)
            continue;
        end
        
        chk_im = im(min_r:max_r,min_c:max_c);
        if max(max(chk_im)) < (1 - 3 * thresh)
            continue;
        else
            % refine centroid max and min
            [chk_r,chk_c] = find(im(min_r:max_r,min_c:max_c) == max(max(chk_im)));% modify
            chk_r = chk_r(1) + min_r-1;
            chk_c = chk_c(1) + min_c-1;
            cr = chk_r;
            cc = chk_c;
            
%                     minimum row calculation
            while im(cr,cc) >  thresh
                cr = cr - 1;
                if cr == 0
                    break;
                end
                if im(cr,cc) <= thresh % .1
                    cc = cc - 1;
                    if im(cr,cc) <= thresh % .1
                        cc = cc + 2;
                    end
                end
            end
            min_r = cr+1;

            cr = chk_r;
            cc = chk_c;
%                     maximum row calculation
            while im(cr,cc) > thresh % .1
                cr = cr + 1;
                if cr > size(im,1)
                    break;
                end
                if im(cr,cc) <= thresh % .1
                    cc = cc - 1;
                    if im(cr,cc) <= thresh % .1
                        cc = cc + 2;
                    end
                end
            end
            max_r = cr-1;

            cr = chk_r;
            cc = chk_c;
%                     mimimum column calculation
            while im(cr,cc) > thresh % .1
                cc = cc - 1;
                if cc == 0
                    break;
                end
                if im(cr,cc) <= thresh % .1
                    cr = cr - 1;
                    if im(cr,cc) <= thresh % .1
                        cr = cr + 2;
                    end
                end
            end
            min_c = cc+1;

            cr = chk_r;
            cc = chk_c;
%                     maximum column calculation
            while im(cr,cc) > thresh % .1
                cc = cc + 1;
                if cc > size(im,2)
                    break;
                end
                if im(cr,cc) <= thresh % .1
                    cr = cr - 1;
                    if im(cr,cc) <= thresh % .1
                        cr = cr + 2;
                    end
                end
            end
            max_c = cc-1;
            
            % update mask data
            mask_part = ones(max_r-min_r+1,max_c-min_c+1);
            mask_im(min_r:max_r,min_c:max_c) = mask_part;
            
            % calculate centriod
            % calculate total centroind intensity
            sum_int = 0;
            for r = min_r:1:max_r
                for c = min_c:1:max_c
                    sum_int = sum_int + im(r,c);
                end
            end
        
            if sum_int == 0
                continue;
            end
            
            % calculate row centroid
            cent_r = 0;
            for r = min_r:1:max_r
                for c = min_c:1:max_c
                    cent_r = cent_r + (r * im(r,c));
                end
            end
            cent_r = cent_r / sum_int;

            % calculate column centroid
            cent_c = 0;
            for c = min_c:1:max_c
                for r = min_r:1:max_r
                    cent_c = cent_c + (c * im(r,c));
                end
            end
            cent_c = cent_c / sum_int;
            
            pts(n,1) = cent_r;
            pts(n,2) = cent_c;
            pts(n,3) = min_r;
            pts(n,4) = max_r;
            pts(n,5) = min_c;
            pts(n,6) = max_c;
            pts(n,7) = im(round(cent_r),round(cent_c));
            
            n = n + 1;
        end
    end
end

centroids_found = toc % timing only

figure;imagesc(im);colormap(gray);% for showing steps only
hold% for showing steps only
for n = 1:1:size(pts,1)% for showing steps only
    plot(pts(n,2),pts(n,1),'r+');% for showing steps only
    plot(pts(n,5),pts(n,3),'b+');% for showing steps only
    plot(pts(n,5),pts(n,4),'b+');% for showing steps only
    plot(pts(n,6),pts(n,3),'b+');% for showing steps only
    plot(pts(n,6),pts(n,4),'b+');% for showing steps only
end% for showing steps only

% figure;imagesc(mask_im);colormap(gray);% for showing steps only

% figure;imagesc(pro_im);colormap(gray);% for showing steps only

%% Calculate centroid statistics (separation and rotation)

% calculate distances and angles between points

p = 1;
for n1 = 1:1:size(pts,1)
    for n2 = 1:1:size(pts,1)
        if n1 == n2
            continue;
        else
            dx = pts(n1,2)-pts(n2,2);
            dy = pts(n1,1)-pts(n2,1);
            d(n1,p) = sqrt(dx^2 + dy^2);
            o(n1,p) = atand(dy/dx);
            p = p + 1;
        end
    end
    p = 1;
end


% find minimum distances and angles

for n = 1:1:size(d,1)
    loc = find(d(n,:) == min(d(n,:)));% this needs to be changed
    if isempty(loc) == 1
        continue;
    end
    min_d_o(n,1) = d(n,loc(1));
    min_d_o(n,2) = o(n,loc(1));
end


% clean up data
% remove extra long distances

av_d = mean(min_d_o(:,1));
pt = 1;
for n = 1:1:size(min_d_o,1)
    if min_d_o(n,1) > av_d
        continue;
    else
        d_o(pt,1) = min_d_o(n,1);
        d_o(pt,2) = min_d_o(n,2);
        pt = pt+1;
    end
end

% remove near 90 degree rotations


for n = 1:1:size(d_o,1)
    if d_o(n,2) > 45
        d_o(n,2) = 90 - d_o(n,2);
    elseif d_o(n,2) < -45
        d_o(n,2) = -90 - d_o(n,2);
    end
end

 
% remove 0 degree rotations

pt = 1;
for n = 1:1:size(d_o,1)
    if d_o(n,2) == 0
        continue;
    else
        dat(pt,1) = d_o(n,1);
        dat(pt,2) = d_o(n,2);
        pt = pt + 1;
    end
end


% calculate rotation angle

min_d_loc = find(dat(:,1) == min(dat(:,1)));

deg_dir = sign(dat(min_d_loc(1),2));

deg = deg_dir * mean(abs(dat(:,2)))

if isequaln(deg,NaN) == 1
    deg = 0;
end


%% Find missing data

% create prediction grid

r_1 = pts(1,1);
c_1 = pts(1,2);

dist = mean(dat(:,1));

sep_h = abs(dist * cosd(deg));
sep_v = abs(dist * sind(deg));

num_step_l = floor(c_1/sep_h);
num_step_r = floor((size(im,2)-c_1)/sep_h);
step_h = num_step_l + num_step_r;

num_step_u = floor(r_1/sep_h);
num_step_d = floor((size(im,1)-r_1)/sep_h);
step_v = num_step_u + num_step_d;

slp = -sign(deg);

if slp == 1
    r_0 = (r_1 - (num_step_l * sep_v)) - (num_step_u * sep_h);
    c_0 = (c_1 - (num_step_l * sep_h)) - (num_step_u * sep_v);
elseif slp == -1
    r_0 = (r_1 + (num_step_l * sep_v)) - (num_step_u * sep_h);
    c_0 = (c_1 - (num_step_l * sep_h)) - (num_step_u * sep_v);
end

n = 1;

r_a = r_0;
c_a = c_0;

step_r = 0;
while r_a <= size(im,1)
    for step_c = 0:1:step_h
        r = r_a + (slp * step_c * sep_v);
        c = c_a + (step_c * sep_h);
        if r < 1 || r > size(im,1)
            continue;
        end
        if c < 1 || c > size(im,2)
            continue;
        end
        chk_grid(n,1) = round(r);
        chk_grid(n,2) = round(c);
        n = n + 1;
    end
    step_r = step_r + 1;
    r_a = r_0 + (step_r * sep_h);
    c_a = c_0 + (-slp * step_r * sep_v);
end

figure;imagesc(im);colormap(gray); % for showing steps
hold on; % for showing steps
plot(chk_grid(:,2),chk_grid(:,1),'g+'); % for showing steps

% Use grid values to search for missing data.

row_rad = floor(min(diff(pts(:,[3 4]),1,2))/2);
col_rad = floor(min(diff(pts(:,[5 6]),1,2))/2);

t_r = min(diff(pts(:,[3 4]),1,2));
t_c = min(diff(pts(:,[5 6]),1,2));

tot_pts = t_r * t_c; % minimum acceptable size of possible data

n = size(pts,1) + 1;

for c_pt = 1:1:size(chk_grid,1)
    min_r = chk_grid(c_pt,1)-row_rad;
    max_r = chk_grid(c_pt,1)+row_rad;
    min_c = chk_grid(c_pt,2)-col_rad;
    max_c = chk_grid(c_pt,2)+col_rad;
    
    next_pt = 0;
    
    %determines if a point is already contained in a centroid
    for chk = 1:1:size(pts,1)
        if (chk_grid(c_pt,1) <= pts(chk,4) && chk_grid(c_pt,1) >= pts(chk,3)) && (chk_grid(c_pt,2) <= pts(chk,6) && chk_grid(c_pt,2) >= pts(chk,5))
            next_pt = 1;
        end
    end
    
    if min_r < 1 || max_r > size(im,1) || min_c < 1 || max_c > size(im,2) || next_pt == 1
        continue;
    end

    chk_im = im(min_r:max_r,min_c:max_c);
    if max(max(chk_im)) < thresh
        continue;
    else
        % refine centroid max and min
        [chk_r,chk_c] = find(im(min_r:max_r,min_c:max_c) == max(max(chk_im)));% modify
        chk_r = chk_r(1) + min_r-1;
        chk_c = chk_c(1) + min_c-1;
        cr = chk_r;
        cc = chk_c;

%                     minimum row calculation
        while im(cr,cc) > thresh
            cr = cr - 1;
            if cr == 0
                break;
            end
            if im(cr,cc) <= thresh % .1
                cc = cc - 1;
                if im(cr,cc) <= thresh % .1
                    cc = cc + 2;
                end
            end
        end
        min_r = cr+1;

        cr = chk_r;
        cc = chk_c;
%                     maximum row calculation
        while im(cr,cc) > thresh % .1
            cr = cr + 1;
            if cr > size(im,1)
                break;
            end
            if im(cr,cc) <= thresh % .1
                cc = cc - 1;
                if im(cr,cc) <= thresh % .1
                    cc = cc + 2;
                end
            end
        end
        max_r = cr-1;

        cr = chk_r;
        cc = chk_c;
%                     mimimum column calculation
        while im(cr,cc) > thresh % .1
            cc = cc - 1;
            if cc == 0
                break;
            end
            if im(cr,cc) <= thresh % .1
                cr = cr - 1;
                if im(cr,cc) <= thresh % .1
                    cr = cr + 2;
                end
            end
        end
        min_c = cc+1;

        cr = chk_r;
        cc = chk_c;
%                     maximum column calculation
        while im(cr,cc) > thresh % .1
            cc = cc + 1;
            if cc > size(im,2)
                break;
            end
            if im(cr,cc) <= thresh % .1
                cr = cr - 1;
                if im(cr,cc) <= thresh % .1
                    cr = cr + 2;
                end
            end
        end
        max_c = cc-1;

        % calculate centriod
        % calculate total centroind intensity
        sum_int = 0;
        sum_pts = 0;
        for r = min_r:1:max_r
            for c = min_c:1:max_c
                sum_int = sum_int + im(r,c);
                sum_pts = sum_pts + 1;
            end
        end
        
        if sum_int < thresh * sum_pts || sum_pts <= tot_pts % thresh * sum_pts
            continue;
        end

        % calculate row centroid
        cent_r = 0;
        for r = min_r:1:max_r
            for c = min_c:1:max_c
                cent_r = cent_r + (r * im(r,c));
            end
        end
        cent_r = cent_r / sum_int;

        % calculate column centroid
        cent_c = 0;
        for c = min_c:1:max_c
            for r = min_r:1:max_r
                cent_c = cent_c + (c * im(r,c));
            end
        end
        cent_c = cent_c / sum_int;
        
        pts(n,1) = cent_r;
        pts(n,2) = cent_c;
        pts(n,3) = min_r;
        pts(n,4) = max_r;
        pts(n,5) = min_c;
        pts(n,6) = max_c;
        pts(n,7) = im(round(cent_r),round(cent_c));

        n = n + 1;

    end
end

%% Find dark/bright "center" of data

m_pts = mean(pts(:,[1 2]));

d_pts = zeros(size(pts,1),3);

for n = 1:1:size(pts,1) % distances from every point to "pre-center"
    d_pts(n,1) = pts(n,1);
    d_pts(n,2) = pts(n,2);
    d_pts(n,3) = sqrt((pts(n,1)-m_pts(1))^2 + (pts(n,2)-m_pts(2))^2);
end

if min(d_pts) < dist/2 % check if "pre-center" exists within current data set
    [val,loc] = min(d_pts);
    cntr = pts(loc,[1 2]);
else % calculate actual center based on 8 closest points (8 based on geometric configuration of screen)
    c_pts = zeros(8,2);
    sort_d_pts = sortrows(d_pts,3);
    c_pts = sort_d_pts(1:8,[1 2]);
    cntr = mean(c_pts);
end

figure;imagesc(im);colormap(gray);% for showing steps only
hold% for showing steps only
for n = 1:1:size(pts,1)% for showing steps only
    plot(pts(n,2),pts(n,1),'r+');% for showing steps only
    plot(pts(n,5),pts(n,3),'b+');% for showing steps only
    plot(pts(n,5),pts(n,4),'b+');% for showing steps only
    plot(pts(n,6),pts(n,3),'b+');% for showing steps only
    plot(pts(n,6),pts(n,4),'b+');% for showing steps only
end% for showing steps only
plot(cntr(2),cntr(1),'gx');


missing_data_corrected = toc % timing only


%% Create screen locations based on configuration data (?)

% input number of holes x/y
num_x = 25; % modify for different methods of input
num_y = 25; % modify for different methods of input

% input hole separation based on pixel (?) data
sep_x = 14;
sep_y = 14; % modify here as well. presumed square arrangement at this point

% generate locations
r_1 = cntr(1);
c_1 = cntr(2);

sep_h = abs(sep_x * cosd(deg));
sep_v = abs(sep_x * sind(deg));

num_step_l = floor(num_x/2);
num_step_r = floor(num_x/2);
num_step_u = floor(num_y/2);
num_step_d = floor(num_y/2);

slp = -sign(deg);

if slp == 1
    r_0 = (r_1 - (num_step_l * sep_v)) - (num_step_u * sep_h);
    c_0 = (c_1 - (num_step_l * sep_h)) - (num_step_u * sep_v);
elseif slp == -1
    r_0 = (r_1 + (num_step_l * sep_v)) - (num_step_u * sep_h);
    c_0 = (c_1 - (num_step_l * sep_h)) - (num_step_u * sep_v);
end

n = 1;

r_a = r_0;
c_a = c_0;

step_v = num_step_u + num_step_d;
step_h = num_step_l + num_step_r;

for step_r = 0:1:step_v+1
    for step_c = 0:1:step_h
        r = r_a + (slp * step_c * sep_v);
        c = c_a + (step_c * sep_h);
        if r < 1 || r > size(im,1)
            continue;
        end
        if c < 1 || c > size(im,2)
            continue;
        end
        scrn_grid(n,1) = round(r);
        scrn_grid(n,2) = round(c);
        n = n + 1;
    end
    r_a = r_0 + (step_r * sep_h);
    c_a = c_0 + (-slp * step_r * sep_v);
end

figure;imagesc(im);colormap(gray);
hold on;
plot(scrn_grid(:,2),scrn_grid(:,1),'g+');

%% Correlation of beamlet and screen data

r0 = cntr(1);
c0 = cntr(2);
s_r0 = ceil(num_y/2);
s_c0 = ceil(num_x/2);
pt = 1;

for n = 1:1:size(pts,1)
     r = pts(n,1);
     c = pts(n,2);
     
     step_r = round((r-r0) / dist); %modify for rotation?
     step_c = round((c-c0) / dist); %modify for rotation?
     
     s_r1 = s_r0 + step_r;
     s_c1 = s_c0 + step_c;
     
     if s_r1 < 1 || s_c1 < 1
         continue;
     end
     
     screen_num = ((s_r1) * num_x) + s_c1;
     
     s_r = scrn_grid(screen_num,1);
     s_c = scrn_grid(screen_num,2);
     
     corr_beamlet(pt,1) = n;
     corr_beamlet(pt,2) = r;
     corr_beamlet(pt,3) = c;
     corr_beamlet(pt,4) = pts(n,3);
     corr_beamlet(pt,5) = pts(n,4);
     corr_beamlet(pt,6) = (pts(n,3) + pts(n,4))/2;
     corr_beamlet(pt,7) = pts(n,5);
     corr_beamlet(pt,8) = pts(n,6);
     corr_beamlet(pt,9) = (pts(n,5) + pts(n,6))/2;
     corr_beamlet(pt,10) = s_r;
     corr_beamlet(pt,11) = s_c;
     pt = pt + 1;
end

figure;imagesc(im);colormap(gray); % for testing purposes
hold on; % for testing purposes
plot(corr_beamlet(:,3),corr_beamlet(:,2),'g+'); % for testing purposes
plot(corr_beamlet(:,11),corr_beamlet(:,10),'r+'); % for testing purposes
plot(scrn_grid(:,2),scrn_grid(:,1),'bx'); % for testing purposes
plot(cntr(2),cntr(1),'c.'); % for testing purposes

%% Consolidate beamlet data with intensity for each point in beamlet

n = 1;

for b_let = 1:1:size(corr_beamlet,1)
    min_r = corr_beamlet(b_let,4);
    max_r = corr_beamlet(b_let,5);
    min_c = corr_beamlet(b_let,7);
    max_c = corr_beamlet(b_let,8);
    for r = min_r:1:max_r
        for c = min_c:1:max_c
            beamlet(n,1) = b_let;
            beamlet(n,2) = r;
            beamlet(n,3) = c;
            beamlet(n,4) = im(r,c);
            n = n + 1;
        end
    end
end

%% Update image mask and apply

for n = 1:1:size(corr_beamlet,1)
    min_r = corr_beamlet(n,4);
    max_r = corr_beamlet(n,5);
    min_c = corr_beamlet(n,7);
    max_c = corr_beamlet(n,8);
    for r = min_r:1:max_r
        for c = min_c:1:max_c
            mask_im(r,c) = 1;
        end
    end
end

pro_im = im .* mask_im; % cleaned image before rotating.

%% Rotate 'corr_beamlet' data


% setup size contstraints for rotated data
sr = size(pro_im,1);
sc = size(pro_im,2);

% setup matrix for rotating every point in corr_beamlet by calculated degree
c_pts_xy = zeros(size(corr_beamlet)); % corr_beamlet initial matrix
c_pts_ro = c_pts_xy; % r/theta initial matrix
n_c_pts_ro = c_pts_xy; % r/theta rotated matrix
n_c_pts_xy = c_pts_xy; % x/y rotated matrix

% center of image defined for rotation - may need to be modified for the
% center of the screen.
cx = cntr(2); % sc/2; screen center (old is image center)
cy = cntr(1); % sr/2; screen center (old is image center)

% populate initial x/y/intensity matrix for conversion to r/theta/intensity
% matrix (centered around centre of image)
for r = 1:1:size(corr_beamlet,1)
    c_pts_xy(r,1) = corr_beamlet(r,1);% beamlet # (constant)
    c_pts_xy(r,2) = corr_beamlet(r,3)-cx+1;% beamlet x centroid
    c_pts_xy(r,3) = corr_beamlet(r,2)-cy+1;% beamlet y centroid
    c_pts_xy(r,4) = corr_beamlet(r,4)-cy+1;% beamlet y minimum
    c_pts_xy(r,5) = corr_beamlet(r,5)-cy+1;% beamlet y maximum
    c_pts_xy(r,6) = corr_beamlet(r,6)-cy+1;% beamlet y center
    c_pts_xy(r,7) = corr_beamlet(r,7)-cx+1;% beamlet x minimum
    c_pts_xy(r,8) = corr_beamlet(r,8)-cx+1;% beamlet x maximum
    c_pts_xy(r,9) = corr_beamlet(r,9)-cx+1;% beamlet x center
    c_pts_xy(r,10) = corr_beamlet(r,11)-cx+1;% beamlet screen x center
    c_pts_xy(r,11) = corr_beamlet(r,10)-cy+1;% beamlet screen y center
end

clear n;

% convert to r/theta matrix
for n = 1:1:size(c_pts_xy,1)
    x = c_pts_xy(n,2);
    y = c_pts_xy(n,3);

    x_min = c_pts_xy(n,7);
    y_min = c_pts_xy(n,4);
    
    x_max = c_pts_xy(n,8);
    y_max = c_pts_xy(n,5);
    
    x_cent = c_pts_xy(n,9);
    y_cent = c_pts_xy(n,6);
    
    scrn_x = c_pts_xy(n,10);
    scrn_y = c_pts_xy(n,11);
    
    r = sqrt((x)^2 + (y)^2);
    theta = abs(atand((y)/(x)));
    
    r_min = sqrt((x_min)^2 + (y_min)^2);
    theta_min = abs(atand((y_min)/(x_min)));
    
    r_max = sqrt((x_max)^2 + (y_max)^2);
    theta_max = abs(atand((y_max)/(x_max)));
    
    r_cent = sqrt((x_cent)^2 + (y_cent)^2);
    theta_cent = abs(atand((y_cent)/(x_cent)));
    
    r_scrn = sqrt((scrn_x)^2 + (scrn_y)^2);
    theta_scrn = abs(atand((scrn_y)/(scrn_x)));
    
    % conditions for rotation depend on initial x/y location relative to
    % center
    if x < 0 && y > 0
        theta = 180 - theta;
    elseif x > 0 && y > 0 
        theta = theta;
    elseif x > 0 && y < 0 
        theta = 360 - theta;
    elseif x < 0 && y < 0
        theta = 180 + theta;
    end
    
    if x_min < 0 && y_min > 0
        theta_min = 180 - theta_min;
    elseif x_min > 0 && y_min > 0 
        theta_min = theta_min;
    elseif x_min > 0 && y_min < 0 
        theta_min = 360 - theta_min;
    elseif x_min < 0 && y_min < 0
        theta_min = 180 + theta_min;
    end
    
    if x_max < 0 && y_max > 0
        theta_max = 180 - theta_max;
    elseif x_max > 0 && y_max > 0 
        theta_max = theta_max;
    elseif x_max > 0 && y_max < 0 
        theta_max = 360 - theta_max;
    elseif x_max < 0 && y_max < 0
        theta_max = 180 + theta_max;
    end
    
    if x_cent < 0 && y_cent > 0
        theta_cent = 180 - theta_cent;
    elseif x_cent > 0 && y_cent > 0 
        theta_cent = theta_cent;
    elseif x_cent > 0 && y_cent < 0 
        theta_cent = 360 - theta_cent;
    elseif x_cent < 0 && y_cent < 0
        theta_cent = 180 + theta_cent;
    end
    
    if scrn_x < 0 && scrn_y > 0
        theta_scrn = 180 - theta_scrn;
    elseif scrn_x > 0 && scrn_y > 0 
        theta_scrn = theta_scrn;
    elseif scrn_x > 0 && scrn_y < 0 
        theta_scrn = 360 - theta_scrn;
    elseif scrn_x < 0 && scrn_y < 0
        theta_scrn = 180 + theta_scrn;
    end
    
    c_pts_ro(n,1) = c_pts_xy(n,1);
    c_pts_ro(n,2) = r;
    c_pts_ro(n,3) = theta;
    c_pts_ro(n,4) = r_min;
    c_pts_ro(n,5) = theta_min;
    c_pts_ro(n,6) = r_max;
    c_pts_ro(n,7) = theta_max;
    c_pts_ro(n,8) = r_cent;
    c_pts_ro(n,9) = theta_cent;
    c_pts_ro(n,10) = r_scrn;
    c_pts_ro(n,11) = theta_scrn;
    
end

% add rotation to r/theta matrix
n_c_pts_ro = c_pts_ro;
n_c_pts_ro(:,3) = c_pts_ro(:,3) + deg;% theta
n_c_pts_ro(:,5) = c_pts_ro(:,5) + deg;% theta min
n_c_pts_ro(:,7) = c_pts_ro(:,7) + deg;% theta max
n_c_pts_ro(:,9) = c_pts_ro(:,9) + deg;% theta cent
n_c_pts_ro(:,11) = c_pts_ro(:,11) + deg;% theta screen

% convert back to x/y form
for  n = 1:1:size(n_c_pts_ro,1)
    r = n_c_pts_ro(n,2);
    theta = n_c_pts_ro(n,3);

    r_min = n_c_pts_ro(n,4);
    theta_min = n_c_pts_ro(n,5);
    
    r_max = n_c_pts_ro(n,6);
    theta_max = n_c_pts_ro(n,7);
    
    r_cent = n_c_pts_ro(n,8);
    theta_cent = n_c_pts_ro(n,9);
    
    r_srcn = n_c_pts_ro(n,10);
    theta_scrn = n_c_pts_ro(n,11);
    
    x = r * cosd(theta) + cx;
    y = r * sind(theta) + cy;

    x_min = r_min * cosd(theta_min) + cx;
    y_min = r_min * sind(theta_min) + cy;
    
    x_max = r_max * cosd(theta_max) + cx;
    y_max = r_max * sind(theta_max) + cy;
    
    x_cent = r_cent * cosd(theta_cent) + cx;
    y_cent = r_cent * sind(theta_cent) + cy;
    
    scrn_x = r_scrn * cosd(theta_scrn) + cx;
    scrn_y = r_scrn * sind(theta_scrn) + cy;
    
    n_c_pts_xy(n,1) = n_c_pts_ro(n,1);
    n_c_pts_xy(n,2) = y;
    n_c_pts_xy(n,3) = x;
    n_c_pts_xy(n,4) = y_min;
    n_c_pts_xy(n,5) = y_max;
    n_c_pts_xy(n,6) = y_cent;
    n_c_pts_xy(n,7) = x_min;
    n_c_pts_xy(n,8) = x_max;
    n_c_pts_xy(n,9) = x_cent;
    n_c_pts_xy(n,10) = scrn_y;
    n_c_pts_xy(n,11) = scrn_x;
end

r_corr_beamlet(:,1) = n_c_pts_xy(:,1);
r_corr_beamlet(:,2) = n_c_pts_xy(:,2)-1;% + abs(min(n_c_pts_xy(:,1)));
r_corr_beamlet(:,3) = n_c_pts_xy(:,3)-1;% + abs(min(n_c_pts_xy(:,2)));
r_corr_beamlet(:,4) = n_c_pts_xy(:,4)-1;% + abs(min(n_c_pts_xy(:,3)));
r_corr_beamlet(:,5) = n_c_pts_xy(:,5)-1;% + abs(min(n_c_pts_xy(:,4)));
r_corr_beamlet(:,6) = n_c_pts_xy(:,6)-1;% + abs(min(n_c_pts_xy(:,5)));
r_corr_beamlet(:,7) = n_c_pts_xy(:,7)-1;% + abs(min(n_c_pts_xy(:,6)));
r_corr_beamlet(:,8) = n_c_pts_xy(:,8)-1;
r_corr_beamlet(:,9) = n_c_pts_xy(:,9)-1;
r_corr_beamlet(:,10) = n_c_pts_xy(:,10)-1;
r_corr_beamlet(:,11) = n_c_pts_xy(:,11)-1;

%% Rotate 'beamlet' data

% setup size contstraints for rotated data
sr = size(pro_im,1);
sc = size(pro_im,2);

% setup matrix for rotating every point in corr_beamlet by calculated degree
c_pts_xy = zeros(size(beamlet)); % corr_beamlet initial matrix
c_pts_ro = c_pts_xy; % r/theta initial matrix
n_c_pts_ro = c_pts_xy; % r/theta rotated matrix
n_c_pts_xy = c_pts_xy; % x/y rotated matrix

% center of image defined for rotation - may need to be modified for the
% center of the screen.
cx = cntr(2); % sc/2; screen center (old is image center)
cy = cntr(1); % sr/2; screen center (old is image center)

% populate initial x/y/intensity matrix for conversion to r/theta/intensity
% matrix (centered around centre of image)
for r = 1:1:size(beamlet,1)
    c_pts_xy(r,1) = beamlet(r,1);% beamlet # (constant)
    c_pts_xy(r,2) = beamlet(r,3)-cx+1;% beamlet x location
    c_pts_xy(r,3) = beamlet(r,2)-cy+1;% beamlet y location
    c_pts_xy(r,4) = beamlet(r,4);% intensity
end

clear n;

% convert to r/theta/intensity matrix
for n = 1:1:size(c_pts_xy,1)
    x = c_pts_xy(n,2);
    y = c_pts_xy(n,3);
    
    r = sqrt((x)^2 + (y)^2);
    theta = abs(atand((y)/(x)));
    
    % conditions for rotation depend on initial x/y location relative to
    % center
    if x < 0 && y > 0
        theta = 180 - theta;
    elseif x > 0 && y > 0 
        theta = theta;
    elseif x > 0 && y < 0 
        theta = 360 - theta;
    elseif x < 0 && y < 0
        theta = 180 + theta;
    end
    
    c_pts_ro(n,1) = c_pts_xy(n,1);
    c_pts_ro(n,2) = r;
    c_pts_ro(n,3) = theta;
    c_pts_ro(n,4) = c_pts_xy(n,4);
    
end

% add rotation to r/theta matrix
n_c_pts_ro = c_pts_ro;
n_c_pts_ro(:,3) = c_pts_ro(:,3) + deg;% theta

% convert back to x/y form
for  n = 1:1:size(n_c_pts_ro,1)
    r = n_c_pts_ro(n,2);
    theta = n_c_pts_ro(n,3);
    
    x = r * cosd(theta) + cx;
    y = r * sind(theta) + cy;
    
    n_c_pts_xy(n,1) = n_c_pts_ro(n,1);
    n_c_pts_xy(n,2) = y;
    n_c_pts_xy(n,3) = x;
    n_c_pts_xy(n,4) = n_c_pts_ro(n,4);
end

r_beamlet(:,1) = n_c_pts_xy(:,1);
r_beamlet(:,2) = n_c_pts_xy(:,2)-1;% + abs(min(n_c_pts_xy(:,1)));
r_beamlet(:,3) = n_c_pts_xy(:,3)-1;% + abs(min(n_c_pts_xy(:,2)));
r_beamlet(:,4) = n_c_pts_xy(:,4);


beamlet_data_rotated = toc % for timing purposes

%% Rotate image

% setup size contstraints for rotated image
sr = size(pro_im,1);
sc = size(pro_im,2);

% setup matrix for rotating every point in image by calculated degree
c_im_xy = zeros(sr*sc,3); % x/y/intensity initial matrix
c_im_ro = c_im_xy; % r/theta/intensity initial matrix
n_c_im_ro = c_im_xy; % r/theta/intensity rotated matrix
n_c_im_xy = c_im_xy; % x/y/intensity rotated matrix

% center of image definced for rotation - may need to be modified for the
% center of the screen.
cx = sc/2; 
cy = sr/2;

c_n = 1;

n = 1;

% populate initial x/y/intensity matrix for conversion to r/theta/intensity
% matrix
for r = 1:1:sr
    for c = 1:1:sc
        c_im_xy(n,1) = c-cx+1;
        c_im_xy(n,2) = r-cy+1;
        c_im_xy(n,3) = pro_im(r,c);
        n = n+1;
    end
end

clear n;

% convert to r/theta/intensity matrix
for n = 1:1:size(c_im_xy,1)
    x = c_im_xy(n,1);
    y = c_im_xy(n,2);

    r = sqrt((x)^2 + (y)^2);
    theta = abs(atand((y)/(x)));
    % conditions for rotation depend on initial x/y location relative to
    % center
    if x < 0 && y > 0
        theta = 180 - theta;
    elseif x > 0 && y > 0 
        theta = theta;
    elseif x > 0 && y < 0 
        theta = 360 - theta;
    elseif x < 0 && y < 0
        theta = 180 + theta;
    end
    c_im_ro(n,1) = r;
    c_im_ro(n,2) = theta;
    c_im_ro(n,3) = c_im_xy(n,3);
end

% add rotation to r/theta/intensity matrix
n_c_im_ro = c_im_ro;
n_c_im_ro(:,2) = c_im_ro(:,2) + deg;

% convert back to x/y/intensity form
for  n = 1:1:size(n_c_im_ro,1)
    r = n_c_im_ro(n,1);
    theta = n_c_im_ro(n,2);

    x = r * cosd(theta) + cx;
    y = r * sind(theta) + cy;

    n_c_im_xy(n,1) = x;
    n_c_im_xy(n,2) = y;
    n_c_im_xy(n,3) = n_c_im_ro(n,3);
end

n_c_im_xy(:,1) = n_c_im_xy(:,1) + abs(min(n_c_im_xy(:,1)));
n_c_im_xy(:,2) = n_c_im_xy(:,2) + abs(min(n_c_im_xy(:,2)));

% convert to image from location (since image is only whole numbers, some
% data may be close, overlap, or be missing
for n = 1:1:size(n_c_im_xy,1)
    x = round(n_c_im_xy(n,1));
    if isequaln(x,NaN)
        x = cx;
    elseif x <= 0
        x = 1;
    end
    y = round(n_c_im_xy(n,2));
    if isequaln(y,NaN)
        y = cy;
    elseif y <= 0
        y = 1;
    end
    v = n_c_im_xy(n,3);
    n_im(y,x) = v;
end

% figure;imagesc(n_im);colormap(gray);% for showing process

% black pixel removeal / fix missing data

for r = 2:1:size(n_im,1)-1
    for c = 2:1:size(n_im,2)-1
        if n_im(r,c) == 0 || isequaln(n_im(r,c),NaN) == 1
            av_i = 0;
            n = 0;
            for nr = -1:1:1
                for nc = -1:1:1
                    if c+nc == c && r+nr == r
                        continue;
                    else
                        v = n_im(r+nr,c+nc);
                        if v == 0 || isequaln(v,NaN) == 1
                            continue
                        else
                            av_i = av_i + v;
                            n = n + 1;
                        end
                    end
                end
            end
            if n > 4
                n_im(r,c) = av_i / n;
            else
                n_im(r,c) = 0;
            end
        end
    end
end

%% Resize and write image

r_dim = size(n_im,1);
c_dim = size(n_im,2);

sized_im = zeros(size_r,size_c);

r_start = round((r_dim - size_r)/2);
c_start = round((c_dim - size_c)/2);

sized_im = n_im(r_start:size_r+r_start-1,c_start:size_c+c_start-1);
n_im = sized_im;


image_rotated = toc % for timing purposes

%% Store data
imwrite(pro_im,['cleaned_',im_str]);
imwrite(n_im,['processed_',im_str]);

c_mat_str = {'beamlet #','centroid row (y)','centroid col (x)','min row','max row','center row','min col','max col','center col','screen center row','screen center col'};
mat_str = {'beamlet #','row (y)','col (x)','intensity'};

writecell(c_mat_str(1:11),['non-rotated_correlated_beamlet_data_for_',im_str(1:end-4),'.xls'],'Sheet',1,'Range','A1');
writematrix(corr_beamlet,['non-rotated_correlated_beamlet_data_for_',im_str(1:end-4),'.xls'],'Sheet',1,'Range','A2');

writecell(c_mat_str(1:11),['rotated_correlated_beamlet_data_for_',im_str(1:end-4),'.xls'],'Sheet',1,'Range','A1');
writematrix(r_corr_beamlet,['rotated_correlated_beamlet_data_for_',im_str(1:end-4),'.xls'],'Sheet',1,'Range','A2');

writecell(mat_str(1:4),['non-rotated_beamlets_for_',im_str(1:end-4),'.xls'],'Sheet',1,'Range','A1');
writematrix(beamlet,['non-rotated_beamlets_for_',im_str(1:end-4),'.xls'],'Sheet',1,'Range','A2');

writecell(mat_str(1:4),['rotated_beamlets_for_',im_str(1:end-4),'.xls'],'Sheet',1,'Range','A1');
writematrix(r_beamlet,['rotated_beamlets_for_',im_str(1:end-4),'.xls'],'Sheet',1,'Range','A2');

%% Display results
figure;
subplot(1,2,1);imagesc(im);colormap(gray);
subplot(1,2,2);imagesc(n_im);colormap(gray);
% figure;imagesc(n_im);colormap(gray);% for showing steps only

program_finished = toc %for timing purposes only
##### SOURCE END #####
--></body></html>