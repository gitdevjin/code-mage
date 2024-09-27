let num = 3;
let string = "hello world"

if (num > 3) {
    console.log("hello world");
} else if (num > 10) {
    console.log(string);
    console.log("Hello OSD!");
} else {
    console.log("hello seneca");
}

for (let i = 1; i <= 5; i++) {
    console.log(i);
}


let sum = 0;
for (let i = 1; i <= 5; i++) {
  sum += i;
}

console.log('Total sum:', sum);

const numbers = [1, 2, 3, 4, 5];
let squaredNumbers = [];

for (let i = 0; i < numbers.length; i++) {
  let square = numbers[i] * numbers[i];
  squaredNumbers.push(square);
}

console.log('Original numbers:', numbers);
console.log('Squared numbers:', squaredNumbers);



console.log("Last Line of test.js")
