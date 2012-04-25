# ulam_matrix returns an ulam spiral of the requested size
#
#
#
#
#

1;

function retval = ring(x,y)
  retval = max(abs([x y]));
endfunction

function retval = ring_lowest(x,y)
  r = ring(x, y);
  retval = (2*r-1) * (2*r-1) + 1;
endfunction

function retval = side_offset(r, s)
  retval = 2*r*s;
endfunction

function retval = ulam_side(x, y)
  retval = 0;
  r = ring(x, y);
  if (y == -r & x != r)
    retval = 1;
  elseif (x == -r & y != -r)
    retval = 2;
  elseif (y == r & x != -r)
    retval = 3;
  endif
endfunction

function d = distance_in(x,y)
  s = ulam_side(x,y);
  r = ring(x,y);
  d = 0;
  if (s == 0)
    d = -y + r;
  elseif (s == 1)
    d = -x + r;
  elseif (s == 2)
    d = y + r;
  elseif (s == 3)
    d = x + r;
  endif
endfunction

function retval = ulam_n(x,y)
  r = ring(x,y);
  s = ulam_side(x,y);
  retval = ring_lowest(x,y) + distance_in(x,y) + side_offset(r,s) -1;
endfunction

function retmatrix = ulam_matrix(s)
  retmatrix = zeros(s);
  h = s
  l = -h
  offset = s +1
  for y = l:h
    for x = l:h
      retmatrix(x + offset, y + offset) = ulam_n(y,x);
    endfor
  endfor
endfunction
