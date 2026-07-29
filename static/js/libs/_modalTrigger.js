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

import { Modal } from 'bootstrap';
import $ from 'jquery';

/**
 * Initialize a Bootstrap modal trigger
 *
 * @param {Object} options
 * @param {string} options.buttonSelector - Selector for trigger button(s)
 * @param {string} options.modalSelector - Selector for modal element
 * @param {Object} options.modalOptions - Bootstrap modal options
 * @returns {Modal|null}
 */
export const initializeModalTrigger = ({
  buttonSelector,
  modalSelector,
  modalOptions = {},
  openOnInit = false,
}) => {
  const btn$ = buttonSelector ? $(buttonSelector) : $();
  const modal$ = $(modalSelector);

  if (!modal$.length) {
    console.warn(`Modal not found: ${modalSelector}`);
    return null;
  }

  const modalInstance = new Modal(modal$.get(0), {
    keyboard: !openOnInit ? false : true,
    backdrop: !openOnInit ? 'static' : '',
    ...modalOptions,
  });

  if (openOnInit) {
    modalInstance.show();
  }

  if (buttonSelector && btn$.length) {
    btn$.off('click.modalTrigger').on('click.modalTrigger', () => {
      modalInstance.show();
    });
  }

  return modalInstance;
};