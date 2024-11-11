import adapter from '@sveltejs/adapter-static';

export default {
    kit: {
        adapter: adapter({
            fallback: 'index.html' // may differ from host to host
        }),
        paths: {
            // relative: true,
            base: '/static'
        }
    }
};