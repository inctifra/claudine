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

import React from "react";
import ReactDOM from "react-dom/client";
import { gooeyToast, GooeyToaster } from "goey-toast";
import "goey-toast/styles.css";

let root = null;

export const ToastProvider = (position = "top-right") => {
    let container = document.getElementById("glowbeauty-homes-toast-root");

    if (!container) {
        container = document.createElement("div");
        container.id = "glowbeauty-homes-toast-root";
        document.body.appendChild(container);
    }

    if (!root) {
        root = ReactDOM.createRoot(container);
    }

    root.render(
        React.createElement(GooeyToaster, {
            position,
        })
    );

};

export const toast = {
  success: (topic = "Success", msg, duration = 3000) =>
    gooeyToast.success(topic, {
      duration,
      description: msg,
    }),

  error: (topic = "Error", msg, duration = 3000) =>
    gooeyToast.error(topic, {
      duration,
      description: msg,
    }),

  loading: (_ = "Loading", msg, duration = 3000) =>
    gooeyToast.loading(msg, {
      duration,
    }),

  custom: (msg, options = {}) => gooeyToast(msg, options),
};