PROGRAM exemplo;
    VAR m: INTEGER;

    FUNCTION f(n: INTEGER; VAR k: INTEGER): INTEGER;
    VAR p, q: INTEGER;
    BEGIN
        IF n < k THEN BEGIN f := n; k := 0 END
                ELSE BEGIN f := f(n - 1, p) + f(n - 2, q); k := p + q + 1 END;

        WRITE(n, k)
    END; (* f *)
BEGIN
    WRITE(f(3, m), m);
END
