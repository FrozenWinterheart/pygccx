Geometry.ExtrudeReturnLateralEntities = 0;
Geometry.CopyMeshingMethod = 1;
Point(1) = {0.1, 0, 0};
Point(2) = {2.0, 0, 0};
Point(3) = {4.0, 0, 0};
Point(4) = {14.0, 0, 0};
Point(5) = {7.0, 7.14142842854285, 0};
Point(6) = {7.0, 9.746794344808963, 0};
Point(7) = {7.0, 11.746794344808963, 0};
Point(8) = {7.0, 60, 0};
Point(9) = {0.1, 60, 0};
Point(10) = {0.1, 11.746794344808963, 0};
Line(1) = {1,2};
Line(2) = {2,3};
Circle(3) = {3,4,5};
Line(4) = {5,6};
Line(5) = {6,7};
Line(6) = {7,8};
Line(7) = {8,9};
Line(8) = {9,10};
Line(9) = {10,1};
Circle(10) = {2,4,6};
Line(11) = {7,10};
Transfinite Curve {:} = 21;
Transfinite Curve {-2,4} = 21 Using Progression 1.1;
Transfinite Curve {3,10} = 21 Using Progression 1.06;
Transfinite Curve {1,5,7,9,11} = 11.0;
Curve Loop(1) = {1,10,5,11,9} ;
Curve Loop(2) = {2,3,4,-10} ;
Curve Loop(3) = {6,7,8,-11} ;
Plane Surface(1) = {1} ;
Plane Surface(2) = {2} ;
Plane Surface(3) = {3} ;
Recombine Surface{:};
Transfinite Surface{:};
Transfinite Surface{1} = {1,2,6,7};
Symmetry {0, 1, 0, 0} {Duplicata { Surface{1,2,3}; }}Transfinite Surface{12} = {1,2,17,21};
ext[] = Extrude { {0,1,0}, {0,0,0}, Pi/180 } { Surface{:}; Layers{1}; Recombine;};
ext[] = Extrude { {0,1,0}, {0,0,0}, 89 *Pi/180}{Surface{ext[0],ext[2],ext[4],ext[6],ext[8],ext[10]}; Layers{20}; Recombine;};
ext[] = Extrude { {0,1,0}, {0,0,0}, Pi/2 } { Surface{ext[0],ext[2],ext[4],ext[6],ext[8],ext[10]}; Layers{20}; Recombine;};
Physical Volume("all") = Volume{:};
Physical Volume("hbv") = {2, 1, 4, 5};
Physical Surface("load") = {88,230,372};
Physical Surface("fix") = {159,301,443};
Physical Surface("sym") = {23,452,12,408,18,430,2,359,1,337,3,381};
Physical Line("hba") = {3,20};
