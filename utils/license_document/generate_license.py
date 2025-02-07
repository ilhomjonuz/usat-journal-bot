async def generate_license(full_name, direction, academic_year_first, academic_year_last, date_year, date_month, order_number, *args, **kwargs):
    from loader import generator

    output_path = f"data/files/license_{full_name.replace(' ', '')}.jpg"

    result = await generator.generate_certificate(
        full_name=full_name,
        direction=direction,
        academic_year_first=academic_year_first,
        academic_year_last=academic_year_last,
        date_year=date_year,
        date_month=date_month,
        order_number=order_number,
        output_path=output_path
    )

    return result
