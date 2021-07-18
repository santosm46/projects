
class Matrix {
    constructor(rows, cols, randnums=false) {
        this.rows = rows;
        this.cols = cols;
        // console.log(`Matrix constr: m[${this.rows}][${this.cols}]`)

        this.data = [];

        for (let i = 0; i < this.rows; i++) {
            const newLine = [];
            for (let j = 0; j < this.cols; j++) {
                newLine.push(randnums ? this.randNum() : 0);
            }
            this.data.push(newLine);
            //this.data.push(new Array(cols));
        }

    }

    randNum() { return Math.random()*2 - 1; }

    getRow(r) {
        return this.data[r];
    }

    getCol(c) {
        const col = [];
        for(let row of this.data) {
            col.push(row[c]);
        }
        return col;
    }

    static fromArray(arr) {
        let m = new Matrix(arr.length, 1);
        for(let i=0; i<arr.length; i++) {
            m.data[i][0] = arr[i];
        }
        return m;
    }

    toArray() {
        const arr = [];
        this.applyFunc((i, j) => {
            arr.push(this.data[i][j]);
        });
        return arr;
    }

    applyFunc(func) {
        for (let i = 0; i < this.rows; i++) {
            for (let j = 0; j < this.cols; j++) {
                func(i, j);
            }
        }
    }

    map(func) {
        this.applyFunc((i, j) => {
            this.data[i][j] = func(this.data[i][j]);
        });
    }

    static map(m, func) {
        let c = m.copy();
        c.map(func);
        return c;
    }

    copy() {
        let copied = new Matrix(this.rows, this.cols);
        copied.applyFunc((i, j) => {
            copied.data[i][j] = this.data[i][j];
        });
        return copied;
    }

    add(value) {
        if(value instanceof Matrix) {
            if(this.rows != value.rows || this.cols != value.cols) {
                console.error(
                    `matrixes of diff sizes: this[${this.rows}][${this.cols}]  m[${value.rows}][${value.cols}]`);
                return;
            }
            this.applyFunc((i,j) => {
                this.data[i][j] += value.data[i][j];
            });
        }
        else {
            this.applyFunc((i,j) => {
                this.data[i][j] += value;
            });
        }
    }

    static subtract(m1, m2) {
        let r = new Matrix(m1.rows, m1.cols);

        r.applyFunc((i,j) => {
            r.data[i][j] = m1.data[i][j] - m2.data[i][j];
        });

        return r;
    }

    static multiply(m1, m2) {
        if(m1.cols !== m2.rows) {
            console.error(`cols is != rows, -> m1[${m1.rows}][${m1.cols}] and m2[${m2.rows}][${m2.cols}]`);
            return undefined;
        }
        let result = new Matrix(m1.rows,m2.cols);
        let m = m1;
        result.applyFunc((i,j) => {
            let sum = 0;
            const row = m.getRow(i);
            const col = m2.getCol(j);
            for(let b=0; b<m.cols; b++) {
                sum += row[b] * col[b];
            }
            result.data[i][j] = sum;
        });
        
        return result;
    }

    multiply(value) {
        if(value instanceof Matrix) {
            
        }
        else {
            this.applyFunc((i,j) => {
                this.data[i][j] *= value;
            });
        }
    }

    static transpose(m) {
        const newMatrix = new Matrix(m.cols, m.rows);
        newMatrix.applyFunc((i,j) => {
            newMatrix.data[i][j] = m.data[j][i];
        });

        return newMatrix;
    }

    transpose() {
        const newMatrix = new Matrix(this.cols, this.rows);
        const original = this;
        newMatrix.applyFunc((i,j) => {
            newMatrix.data[i][j] = original.data[j][i];
        });

        this.data = newMatrix.data;
        this.rows = newMatrix.rows;
        this.cols = newMatrix.cols;
    }

    elementWise(otherMatrix) {
        if(otherMatrix instanceof Matrix) {
            this.applyFunc((i,j) => {
                this.data[i][j] *= otherMatrix.data[i][j];
            });
        }
        else {
            console.log(`otherMatrix must be of type Matrix`);
        }
    }

    randomize() {
        this.applyFunc((i,j) => {
            this.data[i][j] = this.randNum();
        });
    }

    show() {
        console.table(this.data);
    }

    static testMethod() {
        let m = new Matrix(2,2);
        let n = new Matrix(2,2);
        m.randomize(); n.randomize();
        m.show(); n.show();

        // this.add(n);
        // this.elementWise(n);
        let r = Matrix.multiply(m, n);

        console.log('result of m | n');
        r.show();
    }

}


