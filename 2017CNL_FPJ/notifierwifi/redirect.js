// dB, MHz -> meter
function ComputeDistance(signal_level_diff, freq)
{
    return Math.pow(10, 0.05 * signal_level_diff - 4.622) / freq
}

// @corridor
function MyComputeDistance(signal_level_diff, freq)
{
    return Math.pow(10, 0.05 * signal_level_diff + 2.447) / freq
}

// b11: redirect to the web page of AP with max signal level
// return ssid of closest AP
function Redirect1(networks)
{
    var min_distance = MyComputeDistance(-15-networks[0].signal_level, networks[0].frequency);
    var min_j = 0;
    for(var j=1; j<networks.length; j++){
        var distance = MyComputeDistance(-15-networks[j].signal_level, networks[j].frequency);
        //console.log(networks[index[j]].ssid, networks[index[j]].signal_level, networks[index[j]].frequency, distance)
        if(distance < min_distance){
            min_distance = distance;
            min_j = j;
        }
    }
    return networks[min_j].ssid;
}

// AB, AC, BC -> a, b, c
function InitCoordinate(lengths)
{
    var ab2 = Math.pow(lengths[0], 2);
    var ac2 = Math.pow(lengths[1], 2);
    var bc2 = Math.pow(lengths[2], 2);
    var b = (ab2 + bc2 - ac2) / 2 / lengths[0];
    var a = b - lengths[0];
    var c = Math.sqrt(ac2 - Math.pow(a, 2));
    console.log("[a,b,c] = ",a,b,c);
    return [a, b, c];
}

function Quadratic(a, b, c)
{
    if (a == 0)
        throw 'a = 0';
    var delta = Math.pow(b, 2) - 4*a*c;
    if (delta < 0){
        console.log('a =', a, 'b =', b, 'c =', c);
        throw 'delta < 0';
    }
    return [(-b+Math.sqrt(delta))/2/a, (-b-Math.sqrt(delta))/2/a];
}

// [a, b, c], [d1, d2, d3]
function ComputeCoordinate(p, d)
{
    var debug = false;

    var epsilon = 1e-10;

    // Use a, b, c for better readability
    var a = p[0];
    var b = p[1];
    var c = p[2];
    var a2 = Math.pow(a, 2);
    var b2 = Math.pow(b, 2);
    var c2 = Math.pow(c, 2);

    // Check triangle inequality
    var OK = false;
    while (!OK){
        var can_decrease = [true, true, true];
        var err = Math.abs(d[0]-d[1]) - (b-a);
        if (err >= 0){
            if (d[0] > d[1]){
                if(debug) console.log('decrease d[0]');
                d[0] -= (err + epsilon);
                can_decrease[1] = false;
            }
            else{
                if(debug) console.log('decrease d[1]');
                d[1] -= (err + epsilon);
                can_decrease[0] = false;
            }
        }
        err = Math.abs(d[0]-d[2]) - Math.sqrt(a2 + c2);
        if (err >= 0){
            if (d[0] > d[2]){
                if (can_decrease[0]){
                    if(debug) console.log('decrease d[0]');
                    d[0] -= (err + epsilon);
                    can_decrease[2] = false;
                }
                else{
                    if(debug) console.log('increase d[2]');
                    d[2] += (err + epsilon);
                    can_decrease[2] = false;
                }
            }
            else{
                if(debug) console.log('decrease d[2]');
                d[2] -= (err + epsilon);
                can_decrease[0] = false;
            }
        }
        err = Math.abs(d[1]-d[2]) - Math.sqrt(b2 + c2);
        if (err >= 0){
            if (d[1] > d[2]){
                if (can_decrease[1]){
                    if(debug) console.log('decrease d[1]');
                    d[1] -= (err + epsilon);
                    can_decrease[2] = false;
                }
                else{
                    if(debug) console.log('decrease d[0] and d[1]');
                    d[0] -= (err + epsilon);
                    d[1] -= (err + epsilon);
                    can_decrease[2] = false;
                }
            }
            else{
                if (can_decrease[2]){
                    if(debug) console.log('decrease d[2]');
                    d[2] -= (err + epsilon);
                    can_decrease[1] = false;
                }
                else{
                    if(debug) console.log('decrease d[0] and d[2]');
                    d[0] -= (err + epsilon);
                    d[2] -= (err + epsilon);
                    can_decrease[1] = false;
                }
            }
        }
        // Check other triangle inequality
        var err01 = (b - a - d[0] - d[1]) / 2;
        var err02 = (Math.sqrt(a2 + c2) - d[0] - d[2]) / 2;
        var err12 = (Math.sqrt(b2 + c2) - d[1] - d[2]) / 2;
        if (err01 >= 0 || err02 >= 0){
            d[0] += (Math.max(err01, err02) + epsilon);
            if(debug) console.log('increase d[0]');
        }
        if (err01 >= 0 || err12 >= 0){
            d[1] += (Math.max(err01, err12) + epsilon);
            if(debug) console.log('increase d[1]');
        }
        if (err02 >= 0 || err12 >= 0){
            d[2] += (Math.max(err02, err12) + epsilon);
            if(debug) console.log('increase d[2]');
        }

        // Check again
        if (Math.abs(d[0]-d[1]) - (b-a) < 0
            && Math.abs(d[0]-d[2]) - Math.sqrt(a2 + c2) < 0
            && Math.abs(d[1]-d[2]) - Math.sqrt(b2 + c2) < 0)
            OK = true;
    }

    // Square first
    d[0] = Math.pow(d[0], 2);
    d[1] = Math.pow(d[1], 2);
    d[2] = Math.pow(d[2], 2);

    // Compute x1, y1
    var x1 = (d[0] - d[1] + b2 - a2) / 2 / (b-a);
    var y1_arr = Quadratic(1, 0, Math.pow((x1-a), 2) - d[0]);
    var y1;
    if (Math.abs(Math.pow(x1, 2) + Math.pow((y1_arr[0]-c), 2) - d[2])
        > Math.abs(Math.pow(x1, 2) + Math.pow((y1_arr[1]-c), 2) - d[2]))
        y1 = y1_arr[1];
    else
        y1 = y1_arr[0];
    if(debug) console.log('x1 =', x1, 'y1 =', y1);

    // Compute x2, y2
    var temp = d[2] - d[0] - a2 - c2;
    var y2_arr = Quadratic(1 + c2/a2, temp*c/a/a, Math.pow(temp, 2)/4/a/a - d[0]);
    var x2_arr = [0, 0];
    for (var i=0; i<2; i++)
        x2_arr[i] = (temp + 2*c*y2_arr[i])/2/a + a;
    if (Math.abs(Math.pow((x2_arr[0]-b), 2) + Math.pow(y2_arr[0], 2) - d[1])
        > Math.abs(Math.pow((x2_arr[1]-b), 2) + Math.pow(y2_arr[1], 2) - d[1])){
        y2 = y2_arr[1];
        x2 = x2_arr[1];
    }
    else{
        y2 = y2_arr[0];
        x2 = x2_arr[0];
    }
    if(debug) console.log('x2 =', x2, 'y2 =', y2);

    // Compute x3, y3
    temp = d[2] - d[1] - b2 - c2;
    var y3_arr = Quadratic(1 + c2/b2, temp*c/b/b, Math.pow(temp, 2)/4/b/b - d[1]);
    var x3_arr = [0, 0];
    for (var i=0; i<2; i++)
        x3_arr[i] = (temp + 2*c*y3_arr[i])/2/b + b;
    if (Math.abs(Math.pow((x3_arr[0]-a), 2) + Math.pow(y3_arr[0], 2) - d[0])
        > Math.abs(Math.pow((x3_arr[1]-a), 2) + Math.pow(y3_arr[1], 2) - d[0])){
        y3 = y3_arr[1];
        x3 = x3_arr[1];
    }
    else{
        y3 = y3_arr[0];
        x3 = x3_arr[0];
    }
    if(debug) console.log('x3 =', x3, 'y3 =', y3);

    // Final result
    var x = (x1+x2+x3)/3;
    var y = (y1+y2+y3)/3;
    //console.log('x =', x, 'y =', y);

    return [x, y];
}

/* Scenario:
Put AP 7 to the rightmost seat on team 14
Put AP 12 to the leftmost seat on team 4
Put AP 13 to the leftmost seat on team 6
*/

/* Cases:
at the front on the right  => case 0  => Redirect to CNL Lab1 Concept
at the back  on the right  => case 1  => Redirect to CNL Lab1 Experiment
at the front in the middle => case 2  => Redirect to CNL Lab2 Concept
at the back  in the middle => case 3  => Redirect to CNL Lab2 Experiment
at the front on the left   => case 4  => Redirect to CNL Lab3 Concept
at the back  on the left   => case 5  => Redirect to CNL Lab3 Experiment
*/

function Cases(coordinate)
{
    //console.log(coordinate);
    var x = coordinate[0];
    var y = coordinate[1];
    //var x = coordinate[0]-2.26-3.15;
    //var y = coordinate[1]-0.4;
    //console.log(x,y);
    if(isNaN(x) || isNaN(y)){
        throw 'coordinate error';
    }
    if(x >= 0.6 * 10){
        // on the right
        if (y >= 0.6 * 1)
            return 0;
        else
            return 1;
    }
    else if(x >= 0.6 * 1){
        // in the middle
        if (y >= 0.6 * 1)
            return 2;
        else
            return 3;
    }
    else{
        // on the left
        if (y >= 0.6 * 1)
            return 4;
        else
            return 5;
    }
}

// b12: compute current location and redirect to corresponding web page
function Redirect2(networks, points)
{
    // var points = InitCoordinate(lengths);
    var distances = [];
    for(var i=0; i<networks.length; i++){
        distances.push( MyComputeDistance(-15-networks[i].signal_level, networks[i].frequency));
    }
    //console.log("distances = ",distances);
    var coordinate = ComputeCoordinate(points, distances);
    // console.log(coordinate[0], coordinate[1]);
    return Cases(coordinate);
}


exports.Redirect1 = Redirect1
exports.Redirect2 = Redirect2
