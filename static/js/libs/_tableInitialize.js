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

import $ from "jquery";
import DataTable from "datatables.net-dt";
import "datatables.net-responsive-dt";

import "datatables.net-dt/css/datatables.dataTables.css";
import "datatables.net-responsive-dt/css/responsive.dataTables.css";

/**
 * Initialize a DataTable with dynamic config.
 *
 * @param {string} selector - CSS selector for the table.
 * @param {object} options - Custom DataTable configuration.
 * @returns {object} DataTable instance
 */
export function initDynamicDataTable(selector, options = {}) {
  if (!$(selector).get(0)) return;

  const {
    title = null,
    subtitle = null,
    dom = null,
    ...datatableOptions
  } = options;

  const table = new DataTable(selector, {
    responsive: true,
    colReorder: true,
    paging: true,
    pageLength: 5,
    dom:
      dom ||
      (title
        ? "<'row mb-2'<'col-sm-6 table-title'><'col-sm-6'f>>" +
          "<'row'<'col-sm-12'tr>>" +
          "<'row mt-2'<'col-sm-5'i><'col-sm-7'p>>"
        : undefined),

    initComplete: function () {
      if (title) {
        const html = `
          <div>
            <h6 class="mb-0 fw-bold">${title}</h6>
            ${subtitle ? `<small class="text-muted">${subtitle}</small>` : ""}
          </div>
        `;
        $(this.api().table().container()).find(".table-title").html(html);
      }
    },

    ...datatableOptions,
  });

  return table;
}

export const loadTransactionTable = ({
  tableSelector = "#transactionsTable",
  ajaxUrl,
  columns,
}) => {
  // Destroy existing table if initialized
  if ($.fn.DataTable.isDataTable(tableSelector)) {
    $(tableSelector).DataTable().destroy();
    $(tableSelector).empty(); // Clear previous content
  }

  // Default columns if none provided
  const defaultColumns = [
    { data: "holder_name" },
    { data: "holder_email" },
    { data: "tickets_count" },
    { data: "total_quantity" },
    { data: "total_amount" },
  ];

  $(tableSelector).DataTable({
    ajax: {
      url: ajaxUrl,
      dataSrc: function (json) {
        console.log(json);
        return json.data;
      },
    },
    columns: columns || defaultColumns,
    responsive: true,
    paging: true,
    searching: true,
    ordering: true,
  });
};