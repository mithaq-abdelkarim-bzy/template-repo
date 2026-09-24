import * as HX from "hx-model-components";

function vw_post_bind(scale) {
  return (
    <HX.Page title="Post Bind" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="In Progress">
        <HX.Collection
          numCols={3}
          fields={[
            "cds/standard_fields/insured_name.read_only_option",
            "cds/standard_fields/underwriter.read_only_option"
          ]}
        />
        <HX.Pane>
          <HX.Table
            title='APPLICABLE TO ALL SLIP HEADINGS WITHIN THIS SLIP SECTION:'
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_1", labelAlign: "left" },
              { field: "q_2", labelAlign: "left" },
              { field: "q_3", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title='APPLICABLE TO WHOLE SLIP: '
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_4", labelAlign: "left" },
              { field: "q_5", labelAlign: "left" },
              { field: "q_6", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title='CONDITIONS:'
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_7", labelAlign: "left" },
              { field: "q_8", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title='SUBJECTIVITIES:'
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_9", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title='CHOICE OF LAW & JURISDICTION/CONDITIONS: '
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_10", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title='PREMIUM'
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_11", labelAlign: "left" },
              { field: "q_12", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title='INSURER CONTRACT DOCUMENTATION: '
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_13", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title='INFORMATION'
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_14", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="(RE)INSURER' S LIABILITY:"
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_15", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="SIGNING PROVISIONS:"
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_16", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="INSURER'S WRITTEN LINE: "
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_17", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="SLIP LEADER:"
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_18", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="CONTRACT CHANGES:"
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_19", labelAlign: "left" },
              { field: "q_20", labelAlign: "left" },
              { field: "q_21", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="CLAIMS:"
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_22", labelAlign: "left" },
              { field: "q_23", labelAlign: "left" },
              { field: "q_24", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="RULES AND EXTENT OF ANY OTHER DELEGATED CLAIMS AUTHORITY: "
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_25", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="EXPERT(S) FEES COLLECTION: "
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_26", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="OVERSEAS BROKER: "
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_27", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="US CLASSIFICATION:"
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_28", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="CLIENT CLASSIFICATION: "
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_29", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="DISTANCE MARKETING DIRECTIVE: "
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_30", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="DEDUCTIONS"
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_31", labelAlign: "left" },
              { field: "q_32", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="SYNDICATE SPLIT:"
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_33", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
          <HX.Table
            title="Regulatory Risk Location:"
            data={[{ datum: "cds/post_bind/question", maxWidth: 1000 }, { datum: "cds/post_bind/answer", width: 250 }, { datum: "cds/post_bind/comments", width: 500 }]}
            fields={[
              { field: "q_34", labelAlign: "left" }
            ]}
            transpose
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_post_bind };