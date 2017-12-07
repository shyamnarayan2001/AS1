const handleResponse = response => {
  if (!response.ok) throw Error(response.statusText);
  else return response;
};

export const getDisplayName = WrappedComponent => {
  return WrappedComponent.displayName || WrappedComponent.name || "Component";
};

export const wrapDisplayName = (BaseComponent, wrapPrefix) => {
  return `${wrapPrefix}(${getDisplayName(BaseComponent)})`;
};
export const postData = (url, payload) => {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(handleResponse)
    .then(resp => resp.json());
};

export const postFormData = (url,payload) => {
  return fetch(url, {
    method: "POST",
    body: payload
  })
    .then(handleResponse)
    .then(resp => resp.json());

}

export const getData = url => {
  return fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  })
    .then(handleResponse)
    .then(resp => resp.json());
};

export const makeCancelable = promise => {
  let hasCanceled_ = false;

  const wrappedPromise = new Promise((resolve, reject) => {
    promise.then(
      val => (hasCanceled_ ? reject({ isCanceled: true }) : resolve(val)),
      error => (hasCanceled_ ? reject({ isCanceled: true }) : reject(error))
    );
  });

  return {
    promise: wrappedPromise,
    cancel() {
      hasCanceled_ = true;
    }
  };
};

export const compose = (...fns) =>
  fns.reduce((f, g) => (...args) => f(g(...args)));
