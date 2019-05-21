program exemplo6;
    var abc: integer;
    function f(mm,n: integer; function h: integer; var x: integer):integer;
        var s,i:integer;
    begin
        i:=m; s:=a;
        while i<=n
        do begin
            s:=s+h(i);
            i:=i+1; abc:=abc+1
        end;
        f:=s; x:=a
    end(*f*);
    procedure g;
        var abc, b: integer;
        function k1(x: integer): integer;
            begin k1:=x*x end(* k1 *);
        function k2(x:integer): integer;
            begin k2:=k1(k1(x)) end(*k2*);
    begin
        write(f(1,3,k1,a), a);
        write(f(1,2,k2,b), b);
    end (* g *)
begin
    abc:=0;
end.
