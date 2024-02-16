export const loadingPromise = (context, func) => {
  context.commit("setLoading", true);
  return func().finally(() => {
    context.commit("setLoading", false);
  });
};

export default {
  loadingPromise,
}