// Copyright 2026 liont
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     https://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import $ from 'jquery';
import { toast } from './toaster';
export function extractApiError(err) {
  if (err?.response) {
    const data = err.response.data || {};

    return {
      status: err.response.status,
      message: data.error || data.message || data.detail || 'Request failed',
      code: data.code || null,
      raw: data,
    };
  }

  if (err?.request) {
    return {
      status: null,
      message: 'Network error. Please check your connection.',
      code: 'NETWORK_ERROR',
    };
  }

  return {
    status: null,
    message: err?.message || 'Unknown error occurred',
    code: 'UNKNOWN_ERROR',
  };
}

export function setupAjaxForm(selector, { onSuccess, onError, modifyFormData } = {}) {
  $(document).on('submit', selector, async function (e) {
    e.preventDefault();

    const form = $(this);
    const submitBtn = form.find('[type="submit"]');
    const originalBtnHTML = submitBtn.html();

    submitBtn.prop('disabled', true).html(`
      <div class="d-flex align-items-center justify-content-center w-100 h-100 position-relative">
        <span class="spinner-border spinner-border-md text-white me-2" role="status" aria-hidden="true"></span>
      </div>
    `);

    let formData = new FormData(this);

    try {
      if (typeof modifyFormData === 'function') {
        formData = modifyFormData(formData, form) || formData;
      }

      const formValues = Object.fromEntries(formData.entries());
      clearFieldErrors(form);

      const [{ getApiWithHeaders: apiWithHeaders }] = await Promise.all([import('./axios')]);

      const { data } = await apiWithHeaders({
        'Content-Type': 'multipart/form-data',
      }).post(form.attr('action'), formData);

      if (data.success === false) {
        showFieldErrors(form, data.errors);
        if (onError) onError(data, formValues, form);
        return;
      }

      if (onSuccess) onSuccess(data, formValues, form);
    } catch (err) {
      const cleanedError = extractApiError(err);

      if (onError) onError(err, {}, form, cleanedError);
    } finally {
      submitBtn.prop('disabled', false).html(originalBtnHTML);
    }
  });
}

function clearFieldErrors(form) {
  form.find('.error-message').remove();
  form.find('.is-invalid').removeClass('is-invalid');
}

function showFieldErrors(form, errors) {
  if (!errors) return;

  for (const [fieldName, messages] of Object.entries(errors)) {
    const field = form.find(`[name="${fieldName}"]`);

    const msgs = Array.isArray(messages) ? messages : [messages];

    if (field.length) {
      field.addClass('is-invalid');

      const errorDiv = $(
        `<div class="error-message text-danger" style="font-size: 0.85rem;">${msgs.join(
          '<br>'
        )}</div>`
      );

      field.after(errorDiv);
    } else {
      form.prepend(`<div class="alert alert-danger">${msgs.join('<br>')}</div>`);
    }
  }
}

export function handleFormSubmission(selector, callBack) {
  setupAjaxForm(selector, {
    onSuccess(data) {
      console.log(data);
      callBack(data);
    },
    onError(err, _, form, cleanedError) {
      try {
        const html = cleanedError?.raw?.html;

        if (!html) {
          toast.error('Error', 'Something went wrong', 5000);
          callBack(err, cleanedError);
          return;
        }

        const errorData = typeof html === 'string' ? JSON.parse(html) : html;

        const message = errorData?.message || 'Something went wrong';

        toast.error('Failed', message, 5000);

        // callBack(err, cleanedError);
      } catch (error) {
        console.error(error);
        toast.error('Error', 'Something went wrong', 5000);
      }
    },
  });
}