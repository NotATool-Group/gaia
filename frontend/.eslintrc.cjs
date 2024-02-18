module.exports = {
  env: {
    node: true,
  },
  plugins: ["@stylistic/js"],
  extends: ["eslint:recommended", "plugin:vue/vue3-recommended", "prettier"],
  rules: {
    // override/add rules settings here, such as:
    // 'vue/no-unused-vars': 'error'
    "@stylistic/js/max-len": ["warn", { "code": 80 }],
    "vue/block-order": [
      "error",
      {
        order: ["template", "script", "style"],
      },
    ],
    "vue/html-closing-bracket-newline": [
      "warn",
      {
        "singleline": "never",
        "multiline": "never",
        "selfClosingTag": {
          "singleline": "never",
          "multiline": "never",
        },
      },
    ],
  },
};
