export default {
  required(field_name) {
    return (value) => !!value || `${field_name} is required.`;
  },
  email() {
    return (value) => {
      const pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
      return pattern.test(value) || "Invalid e-mail.";
    };
  },
  min_length(length, field_name) {
    return (value) => {
      return (
        value.length >= length ||
        `${field_name} must be at least ${length} characters.`
      );
    };
  },
  max_length(length, field_name) {
    return (value) => {
      return (
        value.length <= length ||
        `${field_name} must be at most ${length} characters.`
      );
    };
  },
};
