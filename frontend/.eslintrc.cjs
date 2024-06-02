module.exports = {
    env: { es2021: true, browser: true, node: true },
    extends: ['plugin:vue/vue3-essential', '@vue/eslint-config-airbnb'],
    plugins: ['import', 'vue'],
    settings: { 'import/resolver': { node: { extensions: ['.js', '.vue'] } } },
    rules: {
        'linebreak-style': 0,
        'class-methods-use-this': 0,
        'import/prefer-default-export': 0,
        'import/no-unresolved': 0,
        'import/extensions': 0,
        'object-curly-newline': 0,
        camelcase: 0,
        'no-undef': 0,
        'no-use-before-define': 0,
        'consistent-return': 0,
        'arrow-parens': 0,
        'vue/multi-word-component-names': 0,
        'no-shadow': 0,
        'vue/max-len': [
            'warn',
            {
                code: 120,
                template: 250,
            },
        ],
        'no-param-reassign': 'warn',
        'vuejs-accessibility/no-redundant-roles': 0,
        'import/no-extraneous-dependencies': 0,
    },
};