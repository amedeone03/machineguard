from machineguard.data.ingestion import ingest_feature_csv


def main():
    ingest_feature_csv(
        csv_path="data/processed/ims_set1_bearing4_x_features.csv",
        bearing_id=1,
    )


if __name__ == "__main__":
    main()