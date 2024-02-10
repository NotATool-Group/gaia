module.exports = {
  env: {
    node: true,
  },
  extends: ["eslint:recommended", "plugin:vue/vue3-recommended", "prettier"],
  rules: {
    // override/add rules settings here, such as:
    // 'vue/no-unused-vars': 'error'
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
