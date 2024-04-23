## Simple Deep learning application

[Deep learning](#https://en.wikipedia.org/wiki/Deep_learning) is an algorithm inspired by how 🧠 works. It distinguishes itself in the identification of patterns across various forms of data, including but not limited to images, text, and sound. It uses forward and backward propagation to find parameters (weights and biases) that minimize the cost function, which is a metric that measures how far off its predictions are from the actual answer(label). Here I created two simple deep learning models to identify cat images and hand-written digits (0-9), respectively. 


- Forward propagation for layer $l$: $a^{[l-1]}\rightarrow a^{[l]}, z^{[l]}, w^{[l]}, b^{[l]}$

  $Z^{[l]} = W^{[l]} A^{[l-1]} + b^{[l]}$
  $A^{[l]} = g^{[l]} (Z^{[l]})$
  (for $i=1,\dots,L$ with initial value $A^{[0]} = X$)

- Backward propagation for layer $l$: $da^{[l]} \rightarrow da^{[l-1]},dW^{[l]}, db^{[l]}$

  $dZ^{[l]} = dA^{[l]} * {g^{[l]}}^{'}(Z^{[l]})$
  $dW^{[l]} = \frac{1}{m}dZ^{[l]}{A^{[l-1]}}^T$
  $db^{[l]} = \frac{1}{m}np.sum(dZ^{[l]}, axis=1, keepdims=True)$
  $dA^{[l-1]} = {W^{[l]}}^T dZ^{[l]} = \frac{dJ}{dA^{[l-1]}} = \frac{dZ^{[l]}}{dA^{[l-1]}} \frac{dJ}{dZ^{[l]}} = \frac{dZ^{[l]}}{dA^{[l-1]}} dZ^{[l]}$
  (with initial value $dZ^{[L]} = A^{[L]}-Y$)


### Typescript (optional)

- Download  & install nodejs 20.12.2

```sh
npm create vite@latest
  ? Project name: lesson11
  > choose Vanilla, TypeScript
```

- Edit `package.json` to edit port and dependencies

```json
  "scripts": {
    "dev": "vite --port 4200",
  },

  "dependencies": {
    "axios": "^1.6.8"
  }
```

### Node server

```sh
# install dependencies specified in package.json
# install if package.json changes e.g. project name
npm i
npm run dev
  VITE v5.2.9  ready in 180 ms

  ➜  Local:   http://localhost:4200/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

- Edit code
  - Write `index.html`
  - Create directory: `./model`, `./templates`
  - Define models and templates
  - Edit `main.ts`

